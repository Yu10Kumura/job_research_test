"""
シンプル求人抽出器 - HTMLから直接全求人を取得
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class SimpleJobExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_all_jobs(self, url: str) -> List[Dict[str, str]]:
        """
        HTMLから直接全求人を抽出
        """
        print(f"🔍 求人データを取得中: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            
            # 複数のエンコーディングを試す
            encodings = ['euc-jp', 'shift_jis', 'utf-8']
            soup = None
            
            for encoding in encodings:
                try:
                    response.encoding = encoding
                    soup = BeautifulSoup(response.text, 'html.parser')
                    test_text = soup.get_text()[:1000]
                    
                    # 文字化けチェック - 日本語の文字が正しく表示されているか
                    if '�' not in test_text and any(char in test_text for char in 'あいうえおかきくけこ'):
                        print(f"✅ エンコーディング {encoding} で読み込み成功")
                        break
                    
                except:
                    continue
            
            if not soup:
                print("⚠️ 適切なエンコーディングが見つからないため、UTF-8で処理を続行")
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
            
            # 求人リンクから情報を抽出
            jobs = self._extract_jobs_from_links(soup, url)
            
            print(f"📊 抽出完了: {len(jobs)}件の求人を取得")
            return jobs
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            return []
    
    def _extract_jobs_from_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """
        求人リンクから情報を抽出
        """
        jobs = []
        
        # job_codeを含むリンクを全て取得
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # job_codeが含まれているリンクのみ処理
            if 'job_code=' in href:
                try:
                    # job_codeを抽出
                    job_code_match = re.search(r'job_code=(\d+)', href)
                    if job_code_match:
                        job_code = job_code_match.group(1)
                        
                        # リンクのテキストを取得（これが求人タイトル）
                        title = link.get_text().strip()
                        
                        # 空でない、適切な長さのタイトルのみ採用
                        if title and len(title) > 5 and len(title) < 300:
                            # 完全なURLを構築
                            if href.startswith('http'):
                                job_url = href
                            else:
                                job_url = f"https://progres02.jposting.net/pgmitsubishielectric/u/{href}"
                            
                            # 基本的な情報を含む求人オブジェクトを作成
                            job_info = {
                                'title': self._clean_title(title),
                                'url': job_url,
                                'job_code': job_code,
                                'source': 'direct_html'
                            }
                            
                            # 重複チェック
                            if not any(job['job_code'] == job_code for job in jobs):
                                jobs.append(job_info)
                                
                                # 進捗表示（最初の10件）
                                if len(jobs) <= 10:
                                    print(f"  {len(jobs):3d}. {title[:70]}...")
                
                except Exception as e:
                    print(f"  ⚠️ リンク解析エラー: {e}")
                    continue
        
        return jobs
    
    def _clean_title(self, title: str) -> str:
        """
        求人タイトルをクリーンアップ
        """
        if not title:
            return ""
        
        # 複数の空白を1つにまとめる
        title = re.sub(r'\s+', ' ', title)
        
        # 前後の空白を削除
        title = title.strip()
        
        # 長すぎる場合は切り詰め
        if len(title) > 200:
            title = title[:197] + "..."
        
        return title
    
    def get_job_categories(self, jobs: List[Dict[str, str]]) -> Dict[str, int]:
        """
        求人のカテゴリ別集計を取得
        """
        categories = {
            'エンジニア系': 0,
            'ビジネス系': 0,
            '製造・生産系': 0,
            'IT・デジタル系': 0,
            'その他': 0
        }
        
        for job in jobs:
            title = job['title'].lower()
            
            if any(keyword in title for keyword in ['エンジニア', '開発', '設計', '技術']):
                categories['エンジニア系'] += 1
            elif any(keyword in title for keyword in ['営業', '企画', '人事', '採用', 'マーケティング']):
                categories['ビジネス系'] += 1
            elif any(keyword in title for keyword in ['製造', '生産', '品質', '組立']):
                categories['製造・生産系'] += 1
            elif any(keyword in title for keyword in ['it', 'システム', 'ai', 'dx', 'デジタル']):
                categories['IT・デジタル系'] += 1
            else:
                categories['その他'] += 1
        
        return categories

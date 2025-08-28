"""
全求人取得器 - 三菱電機JPOSTING用
377件すべての求人を取得・解析する
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Set
import time
from urllib.parse import urljoin, urlparse, parse_qs
import logging

class CompleteJobExtractor:
    def __init__(self):
        self.base_url = "https://progres02.jposting.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.all_jobs: List[Dict[str, str]] = []
        self.job_codes: Set[str] = set()
        
    def extract_all_jobs(self, start_url: str) -> List[Dict[str, str]]:
        """
        377件すべての求人を取得
        """
        print("🚀 全求人取得を開始...")
        
        # Step 1: メインページからすべての求人コードを収集
        self._collect_all_job_codes(start_url)
        
        print(f"📊 発見した求人コード数: {len(self.job_codes)}件")
        
        # Step 2: 各求人の詳細情報を取得
        self._fetch_job_details()
        
        print(f"✅ 取得完了: {len(self.all_jobs)}件の求人データを取得")
        return self.all_jobs
    
    def _collect_all_job_codes(self, url: str):
        """
        すべての求人コードを収集
        """
        try:
            print(f"🔍 求人コード収集中: {url}")
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 求人へのリンクを全て取得
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # job_codeパラメータがあるリンクを探す
                if 'job_code=' in href:
                    # job_codeを抽出
                    match = re.search(r'job_code=(\d+)', href)
                    if match:
                        job_code = match.group(1)
                        self.job_codes.add(job_code)
                        
                        # デバッグ: 最初の10件のリンクテキストを表示
                        if len(self.job_codes) <= 10:
                            link_text = link.get_text().strip()[:50]
                            print(f"  求人コード{job_code}: {link_text}...")
            
            print(f"📝 メインページから {len(self.job_codes)}件の求人コードを発見")
            
            # もし377件に満たない場合、検索やフィルタを試す
            if len(self.job_codes) < 300:
                print("⚠️ 求人数が少ないため、追加の検索を実行...")
                self._try_additional_searches(url)
                
        except Exception as e:
            print(f"❌ 求人コード収集エラー: {e}")
    
    def _try_additional_searches(self, base_url: str):
        """
        追加の検索パターンを試行
        """
        # 異なる検索条件やソート順で試行
        search_params = [
            '',  # デフォルト
            '?search=1',  # 検索実行
            '?sort=new',  # 新着順
            '?sort=code', # コード順
        ]
        
        for param in search_params:
            try:
                test_url = base_url + param
                print(f"  🔍 追加検索: {test_url}")
                
                response = self.session.get(test_url, timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                original_count = len(self.job_codes)
                
                # 新しい求人コードを探す
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'job_code=' in href:
                        match = re.search(r'job_code=(\d+)', href)
                        if match:
                            self.job_codes.add(match.group(1))
                
                new_count = len(self.job_codes)
                if new_count > original_count:
                    print(f"    ✅ {new_count - original_count}件の追加求人を発見")
                
                time.sleep(0.5)  # レート制限
                
            except Exception as e:
                print(f"    ❌ 追加検索エラー: {e}")
    
    def _fetch_job_details(self):
        """
        各求人の詳細情報を取得
        """
        print("🔄 求人詳細情報を取得中...")
        
        for i, job_code in enumerate(sorted(self.job_codes), 1):
            try:
                # プログレス表示
                if i % 50 == 0 or i <= 10:
                    print(f"  📋 進捗: {i}/{len(self.job_codes)} ({i/len(self.job_codes)*100:.1f}%)")
                
                job_url = f"{self.base_url}/pgmitsubishielectric/u/job.phtml?job_code={job_code}"
                
                response = self.session.get(job_url, timeout=10)
                
                # エンコーディングを複数試行
                encodings = ['utf-8', 'shift_jis', 'euc-jp', 'iso-2022-jp']
                soup = None
                
                for encoding in encodings:
                    try:
                        response.encoding = encoding
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # 文字化けチェック: 日本語が正しく表示されているか
                        test_text = soup.get_text()[:500]
                        if '�' not in test_text and any(char in test_text for char in 'あいうえお'):
                            break
                    except:
                        continue
                
                if not soup:
                    # フォールバック: 生のHTMLから抽出を試行
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='shift_jis')
                
                # 求人情報を抽出
                job_info = self._parse_job_page(soup, job_url, job_code)
                
                if job_info:
                    self.all_jobs.append(job_info)
                    
                    # 最初の数件の詳細をログ出力
                    if len(self.all_jobs) <= 5:
                        print(f"    ✅ {job_info['title'][:60]}...")
                
                # レート制限（1秒間に2リクエスト程度）
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ❌ 求人コード{job_code}の取得エラー: {e}")
                continue
    
    def _parse_job_page(self, soup: BeautifulSoup, url: str, job_code: str) -> Dict[str, str]:
        """
        個別求人ページから情報を抽出
        """
        try:
            # タイトル抽出
            title = self._extract_job_title(soup)
            if not title:
                return None
            
            # 説明文抽出
            description = self._extract_job_description(soup)
            
            # 勤務地抽出
            location = self._extract_job_location(soup)
            
            # 職種・カテゴリ抽出
            category = self._extract_job_category(soup)
            
            return {
                'title': title,
                'url': url,
                'job_code': job_code,
                'description': description or "詳細情報なし",
                'location': location or "勤務地不明",
                'category': category or "カテゴリ不明",
                'source': 'jposting_complete'
            }
            
        except Exception as e:
            print(f"      ❌ 求人詳細解析エラー: {e}")
            return None
    
    def _extract_job_title(self, soup: BeautifulSoup) -> str:
        """求人タイトルを抽出"""
        # h2タグから抽出（最も可能性が高い）
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags:
            text = h2.get_text().strip()
            if text and len(text) > 5 and self._looks_like_job_title(text):
                return self._clean_title(text)
        
        # h1タグから抽出
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text().strip()
            if text and len(text) > 5 and text != '求人詳細':
                return self._clean_title(text)
        
        # テーブルの最初の行から抽出を試行
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[:3]:  # 最初の3行をチェック
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    # 2列目（職種名列）をチェック
                    title_text = cells[1].get_text().strip()
                    if self._looks_like_job_title(title_text):
                        return self._clean_title(title_text)
        
        # フォールバック: ページ内の長めのテキストから推測
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        for line in lines[:30]:  # 最初の30行から探す
            if self._looks_like_job_title(line) and len(line) > 10:
                return self._clean_title(line)
        
        # 最終フォールバック: job_codeから生成
        return f"求人番号_{soup.find('input', {'name': 'job_code'}) or 'unknown'}"
    
    def _extract_job_description(self, soup: BeautifulSoup) -> str:
        """求人説明を抽出"""
        # 説明が含まれていそうな要素を探す
        desc_selectors = [
            '.job-description',
            '.description', 
            '.content',
            '.detail',
            '[class*="desc"]',
            'p'
        ]
        
        descriptions = []
        for selector in desc_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if len(text) > 50 and len(text) < 1000:  # 適切な長さ
                    descriptions.append(text)
        
        if descriptions:
            # 最も詳細な説明を選択
            return max(descriptions, key=len)[:500]  # 500文字まで
        
        return None
    
    def _extract_job_location(self, soup: BeautifulSoup) -> str:
        """勤務地を抽出"""
        location_keywords = ['勤務地', '所在地', '勤務先', '場所', '東京', '大阪', '神戸', '製作所']
        
        all_text = soup.get_text()
        lines = all_text.split('\\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line for keyword in location_keywords):
                if len(line) < 100:  # 長すぎない
                    return line
        
        return None
    
    def _extract_job_category(self, soup: BeautifulSoup) -> str:
        """職種カテゴリを抽出"""
        category_keywords = {
            'エンジニア': 'エンジニア系',
            '開発': 'エンジニア系', 
            '設計': 'エンジニア系',
            '営業': 'ビジネス系',
            '企画': 'ビジネス系',
            '人事': 'ビジネス系',
            'マーケティング': 'ビジネス系',
            '製造': '製造系',
            '品質': '製造系',
            '生産': '製造系'
        }
        
        all_text = soup.get_text().lower()
        
        for keyword, category in category_keywords.items():
            if keyword.lower() in all_text:
                return category
        
        return None
    
    def _looks_like_job_title(self, text: str) -> bool:
        """テキストが求人タイトルらしいかチェック"""
        if not text or len(text) < 10 or len(text) > 200:
            return False
        
        job_indicators = [
            '【', '】', 'エンジニア', '技術者', '開発', '設計', '営業', 
            '企画', '管理', 'システム', 'ソフト', '製造', 'プロジェクト',
            'WEB面接', '東京', '大阪', '神戸', '製作所', '担当', '主任'
        ]
        
        return any(indicator in text for indicator in job_indicators)
    
    def _clean_title(self, title: str) -> str:
        """求人タイトルをクリーンアップ"""
        if not title:
            return ""
        
        # 不要な文字を除去
        title = re.sub(r'\\s+', ' ', title)
        title = re.sub(r'\\n+', ' ', title) 
        title = title.strip()
        
        # 長すぎる場合は切り詰め
        if len(title) > 150:
            title = title[:147] + "..."
        
        return title

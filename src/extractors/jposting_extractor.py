"""
JPOSTING求人抽出器 - 三菱電機用
https://progres02.jposting.net/pgmitsubishielectric/u/job.phtml から求人情報を抽出
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import time

class JPOSTINGExtractor:
    def __init__(self):
        self.base_url = "https://progres02.jposting.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_jobs(self, url: str) -> List[Dict[str, str]]:
        """
        求人一覧URLから求人情報を抽出
        """
        try:
            print(f"🔍 求人ページにアクセス中: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 文字エンコーディングを明示的に設定
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            
            # 求人情報を探す - 職種名のパターンを探索
            # サイト構造から、職種名は様々な形式で表示されている
            job_elements = self._find_job_elements(soup)
            
            print(f"📋 {len(job_elements)}件の求人を発見")
            
            for i, element in enumerate(job_elements):
                try:
                    job_info = self._parse_job_element(element)
                    if job_info:
                        jobs.append(job_info)
                        print(f"  {i+1}. {job_info['title'][:50]}...")
                        
                        # 最大5件まで
                        if len(jobs) >= 5:
                            print("  ⚠️ 5件に達したため抽出を停止")
                            break
                            
                except Exception as e:
                    print(f"  ⚠️ 求人 {i+1} の解析エラー: {e}")
                    continue
            
            return jobs
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"サイトへのアクセスエラー: {e}")
        except Exception as e:
            raise Exception(f"求人抽出エラー: {e}")
    
    def _find_job_elements(self, soup: BeautifulSoup) -> List:
        """
        求人要素を見つける
        """
        job_elements = []
        
        # パターン1: テーブル形式の求人情報
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:  # 職種名と勤務地がある行
                    job_elements.append(row)
        
        # パターン2: リスト形式
        lists = soup.find_all(['ul', 'ol'])
        for ul in lists:
            items = ul.find_all('li')
            for item in items:
                if item.get_text().strip():  # 空でないアイテム
                    job_elements.append(item)
        
        # パターン3: div要素で構成されている場合
        divs = soup.find_all('div')
        for div in divs:
            # 求人タイトルらしいテキストが含まれているdiv
            text = div.get_text().strip()
            if any(keyword in text for keyword in ['【', 'エンジニア', '技術', '営業', '管理']):
                if len(text) > 10 and len(text) < 200:  # 適切な長さ
                    job_elements.append(div)
        
        # パターン4: 直接テキストをスキャン
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for line in lines:
            line = line.strip()
            if self._looks_like_job_title(line):
                # 疑似要素として作成
                fake_element = type('Element', (), {
                    'get_text': lambda: line,
                    'find': lambda *args: None,
                    'find_all': lambda *args: []
                })()
                job_elements.append(fake_element)
        
        # 重複除去と絞り込み
        unique_jobs = []
        seen_titles = set()
        
        for element in job_elements:
            text = element.get_text().strip()
            if text and text not in seen_titles and self._looks_like_job_title(text):
                seen_titles.add(text)
                unique_jobs.append(element)
                if len(unique_jobs) >= 10:  # 最大10件を候補とする
                    break
        
        return unique_jobs
    
    def _looks_like_job_title(self, text: str) -> bool:
        """
        テキストが求人タイトルっぽいかを判定
        """
        if not text or len(text) < 5 or len(text) > 150:
            return False
        
        # 求人タイトルの特徴
        job_indicators = [
            '【', 'エンジニア', '技術者', '設計', '開発', '管理', '営業',
            '担当', 'スタッフ', '職', '業務', '責任者', 'マネージャー',
            '製作所', '事業所', 'NEW', '経験', '未経験', 'WEB面接'
        ]
        
        # 除外パターン
        exclude_patterns = [
            '職種名', '勤務地', '応募', '選考', '面接', '説明会',
            '動画', 'YouTube', 'http', 'www', 'Copyright', '©',
            '全国', '北海道', '東京', '大阪', '神奈川'  # 単独の地名は除外
        ]
        
        # 除外パターンにマッチするかチェック
        for exclude in exclude_patterns:
            if exclude in text and len(text.replace(exclude, '').strip()) < 5:
                return False
        
        # 求人指標が含まれているかチェック
        return any(indicator in text for indicator in job_indicators)
    
    def _parse_job_element(self, element) -> Dict[str, str]:
        """
        求人要素から情報を抽出
        """
        # タイトル取得
        title = self._extract_title(element)
        if not title:
            return None
        
        # URL取得の試行
        job_url = self._extract_url(element)
        
        return {
            'title': title,
            'url': job_url
        }
    
    def _extract_title(self, element) -> str:
        """
        求人タイトルを抽出
        """
        # 要素からテキストを取得
        try:
            title = element.get_text().strip()
        except:
            return None
        
        # 文字化け対策 - デコードの試行
        if title and ('�' in title or len(title.encode('utf-8', errors='ignore')) < len(title) * 0.5):
            # 文字化けしている可能性が高い場合はスキップ
            return None
        
        # クリーンアップ
        title = re.sub(r'\s+', ' ', title)  # 複数の空白を1つに
        title = re.sub(r'\n+', ' ', title)  # 改行を空白に
        
        # 長すぎる場合は最初の部分のみを使用
        lines = title.split(' ')
        if len(title) > 100 and len(lines) > 3:
            title = ' '.join(lines[:3]) + "..."
        elif len(title) > 100:
            title = title[:97] + "..."
        
        return title if title and len(title) > 5 else None
    
    def _extract_url(self, element) -> str:
        """
        求人詳細URLを抽出（試行）
        """
        # デフォルトURL（詳細ページが見つからない場合）
        default_url = "https://progres02.jposting.net/pgmitsubishielectric/u/job.phtml"
        
        try:
            # リンク要素を探す
            link = element.find('a')
            if link and link.get('href'):
                href = link.get('href')
                if href.startswith('http'):
                    return href
                elif href.startswith('/'):
                    return self.base_url + href
                else:
                    return self.base_url + '/' + href
            
            # 親要素にリンクがあるかチェック
            parent = getattr(element, 'parent', None)
            if parent:
                parent_link = parent.find('a')
                if parent_link and parent_link.get('href'):
                    href = parent_link.get('href')
                    if href.startswith('http'):
                        return href
                    elif href.startswith('/'):
                        return self.base_url + href
            
            # デフォルトURLを返す
            return default_url
            
        except Exception:
            return default_url

def extract_jobs_from_url(url: str) -> List[Dict[str, str]]:
    """
    外部インターフェース: URLから求人情報を抽出
    """
    extractor = JPOSTINGExtractor()
    return extractor.extract_jobs(url)

if __name__ == "__main__":
    # テスト実行
    url = "https://progres02.jposting.net/pgmitsubishielectric/u/job.phtml"
    
    try:
        print("🚀 JPOSTING求人抽出器 - テスト実行")
        print(f"対象URL: {url}")
        print("-" * 60)
        
        jobs = extract_jobs_from_url(url)
        
        print(f"\n✅ 抽出完了: {len(jobs)}件の求人")
        print("=" * 60)
        
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   URL: {job['url']}")
        
        print("\n" + "=" * 60)
        print("🎉 テスト完了")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

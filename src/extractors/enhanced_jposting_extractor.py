"""
強化版JPOSTING求人抽出器 - 階層探索機能付き
すべての求人を階層的に探索して取得
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Set
import time
from urllib.parse import urljoin, urlparse
import logging

class EnhancedJPOSTINGExtractor:
    def __init__(self, max_jobs: int = 50, max_depth: int = 3):
        self.base_url = "https://progres02.jposting.net"
        self.max_jobs = max_jobs
        self.max_depth = max_depth
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.found_jobs: List[Dict[str, str]] = []
        
    def extract_all_jobs(self, start_url: str) -> List[Dict[str, str]]:
        """
        開始URLから階層的にすべての求人を探索・抽出
        """
        print(f"🚀 階層探索開始: {start_url}")
        print(f"📋 最大求人数: {self.max_jobs}件, 最大階層: {self.max_depth}")
        
        self.found_jobs = []
        self.visited_urls = set()
        
        # 階層探索実行
        self._explore_recursive(start_url, depth=0)
        
        print(f"✅ 探索完了: {len(self.found_jobs)}件の求人を発見")
        return self.found_jobs
    
    def _explore_recursive(self, url: str, depth: int = 0):
        """
        再帰的に階層探索
        """
        # 制限チェック
        if depth > self.max_depth or len(self.found_jobs) >= self.max_jobs:
            return
        
        # 重複チェック
        if url in self.visited_urls:
            return
            
        self.visited_urls.add(url)
        
        try:
            print(f"{'  ' * depth}🔍 探索中 (階層{depth}): {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 現在のページから求人を抽出
            current_jobs = self._extract_jobs_from_page(soup, url, depth)
            self.found_jobs.extend(current_jobs)
            
            # 制限に達した場合は停止
            if len(self.found_jobs) >= self.max_jobs:
                print(f"{'  ' * depth}✋ 最大求人数に達したため停止")
                return
            
            # 次の階層のURLを探索
            if depth < self.max_depth:
                next_urls = self._find_job_related_links(soup, url)
                print(f"{'  ' * depth}🔗 次階層のリンク: {len(next_urls)}件")
                
                for next_url in next_urls[:10]:  # 各階層で最大10リンクまで
                    if len(self.found_jobs) >= self.max_jobs:
                        break
                    time.sleep(0.5)  # レート制限
                    self._explore_recursive(next_url, depth + 1)
                    
        except requests.exceptions.RequestException as e:
            print(f"{'  ' * depth}❌ アクセスエラー: {e}")
        except Exception as e:
            print(f"{'  ' * depth}❌ 解析エラー: {e}")
    
    def _extract_jobs_from_page(self, soup: BeautifulSoup, page_url: str, depth: int) -> List[Dict[str, str]]:
        """
        単一ページから求人情報を抽出
        """
        jobs = []
        
        # パターン1: テーブル形式の求人
        tables = soup.find_all('table')
        for table in tables:
            jobs.extend(self._parse_table_jobs(table, page_url))
        
        # パターン2: リスト形式の求人
        for tag in ['ul', 'ol']:
            lists = soup.find_all(tag)
            for ul in lists:
                jobs.extend(self._parse_list_jobs(ul, page_url))
        
        # パターン3: div要素の求人
        divs = soup.find_all('div', class_=re.compile(r'(job|position|career|recruit)', re.I))
        for div in divs:
            job_info = self._parse_div_job(div, page_url)
            if job_info:
                jobs.append(job_info)
        
        # パターン4: 一般的なdiv要素から求人らしいテキストを探索
        all_divs = soup.find_all('div')
        for div in all_divs:
            text = div.get_text().strip()
            if self._looks_like_job_title(text):
                job_info = self._create_job_info(text, page_url, div)
                if job_info:
                    jobs.append(job_info)
        
        # 重複除去
        unique_jobs = []
        seen_titles = set()
        
        for job in jobs:
            if job['title'] not in seen_titles:
                seen_titles.add(job['title'])
                unique_jobs.append(job)
                if len(unique_jobs) <= 5:  # ログ表示制限
                    print(f"{'  ' * depth}  📄 {job['title'][:60]}...")
        
        print(f"{'  ' * depth}📊 このページから {len(unique_jobs)}件の求人を抽出")
        return unique_jobs
    
    def _parse_table_jobs(self, table, page_url: str) -> List[Dict[str, str]]:
        """テーブルから求人情報を抽出"""
        jobs = []
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 1:
                # 最初のセルを求人タイトルとして扱う
                title_text = cells[0].get_text().strip()
                if self._looks_like_job_title(title_text):
                    # URLを探す
                    link = cells[0].find('a')
                    job_url = urljoin(page_url, link['href']) if link and link.get('href') else page_url
                    
                    jobs.append({
                        'title': self._clean_title(title_text),
                        'url': job_url,
                        'source': 'table'
                    })
        
        return jobs
    
    def _parse_list_jobs(self, ul, page_url: str) -> List[Dict[str, str]]:
        """リストから求人情報を抽出"""
        jobs = []
        items = ul.find_all('li')
        
        for item in items:
            text = item.get_text().strip()
            if self._looks_like_job_title(text):
                link = item.find('a')
                job_url = urljoin(page_url, link['href']) if link and link.get('href') else page_url
                
                jobs.append({
                    'title': self._clean_title(text),
                    'url': job_url,
                    'source': 'list'
                })
        
        return jobs
    
    def _parse_div_job(self, div, page_url: str) -> Dict[str, str]:
        """div要素から求人情報を抽出"""
        text = div.get_text().strip()
        if not self._looks_like_job_title(text):
            return None
        
        link = div.find('a')
        job_url = urljoin(page_url, link['href']) if link and link.get('href') else page_url
        
        return {
            'title': self._clean_title(text),
            'url': job_url,
            'source': 'div'
        }
    
    def _create_job_info(self, text: str, page_url: str, element) -> Dict[str, str]:
        """汎用求人情報作成"""
        if not self._looks_like_job_title(text):
            return None
        
        link = element.find('a') if element else None
        job_url = urljoin(page_url, link['href']) if link and link.get('href') else page_url
        
        return {
            'title': self._clean_title(text),
            'url': job_url,
            'source': 'general'
        }
    
    def _find_job_related_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """求人関連のリンクを探索"""
        links = set()
        
        # すべてのリンクを取得
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            
            # 求人関連のURLかチェック
            if self._is_job_related_url(full_url, link.get_text().strip()):
                links.add(full_url)
        
        # 現在のドメイン内のリンクのみ
        domain_links = []
        current_domain = urlparse(current_url).netloc
        
        for link in links:
            if urlparse(link).netloc == current_domain:
                domain_links.append(link)
        
        return list(domain_links)[:20]  # 最大20リンク
    
    def _is_job_related_url(self, url: str, link_text: str) -> bool:
        """URLが求人関連かどうか判定"""
        job_keywords = [
            'job', 'career', 'recruit', 'position', 'employment',
            '求人', '募集', '採用', '職種', 'キャリア'
        ]
        
        url_lower = url.lower()
        text_lower = link_text.lower()
        
        return any(keyword in url_lower or keyword in text_lower 
                  for keyword in job_keywords)
    
    def _looks_like_job_title(self, text: str) -> bool:
        """テキストが求人タイトルらしいかチェック"""
        if not text or len(text) < 5 or len(text) > 200:
            return False
        
        # 求人タイトルによく含まれるキーワード
        job_indicators = [
            'エンジニア', '技術者', '開発', '設計', '営業', '企画', '管理',
            '【', '】', 'システム', 'ソフト', 'ハード', '製造', '品質',
            'プロジェクト', 'マネージャー', '主任', '課長', '部長', '担当',
            '正社員', '契約', '派遣', 'WEB面接', '東京', '大阪', '神戸'
        ]
        
        return any(indicator in text for indicator in job_indicators)
    
    def _clean_title(self, title: str) -> str:
        """求人タイトルをクリーンアップ"""
        if not title:
            return ""
        
        # 不要な文字を除去
        title = re.sub(r'\s+', ' ', title)  # 複数空白を1つに
        title = re.sub(r'\n+', ' ', title)  # 改行を空白に
        title = title.strip()
        
        # 長すぎる場合は切り詰め
        if len(title) > 150:
            title = title[:147] + "..."
        
        return title

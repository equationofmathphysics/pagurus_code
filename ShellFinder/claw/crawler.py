"""
ShellFinder Crawler Module
爬虫模块 - 负责 GitHub API 数据爬取
"""

import requests
import time
from typing import List, Dict, Optional
import re
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from claw.database import Database


class GitHubCrawler:
    """GitHub API 爬虫类"""

    def __init__(self, token: str = None):
        """初始化爬虫"""
        self.token = token or Config.GITHUB_TOKEN
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'PaGURUS-ShellFinder'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.db = Database()

    def _make_request(self, url: str, params: dict = None) -> Optional[Dict]:
        """发送 GitHub API 请求"""
        try:
            response = self.session.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()

            # 检查剩余配额
            remaining = response.headers.get('X-RateLimit-Remaining', 'unknown')
            if Config.GITHUB_TOKEN:
                print(f"  [Rate Limit] Remaining: {remaining} requests")

            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"  [Error] Rate limit exceeded. Please wait or add a GitHub token.")
            elif e.response.status_code == 404:
                print(f"  [Error] Resource not found: {url}")
            else:
                print(f"  [Error] HTTP {e.response.status_code}: {e}")
            return None

        except Exception as e:
            print(f"  [Error] Request failed: {e}")
            return None

    def _parseAwesome_list_readme(self, readme_content: str) -> List[Dict]:
        """解析 Awesome List 的 README 内容，提取仓库链接"""
        repos = []

        # 匹配 Markdown 链接格式: [text](url)
        # GitHub 仓库链接格式: https://github.com/owner/repo
        pattern = r'\[([^\]]+)\]\((https://github\.com/[^/]+/[^)\s]+)\)'

        matches = re.findall(pattern, readme_content)

        for text, url in matches:
            # 提取 owner/repo
            if 'github.com/' in url:
                parts = url.split('github.com/')[-1].split('/')
                if len(parts) >= 2:
                    owner = parts[0]
                    repo_name = parts[1].replace('.git', '')

                    repos.append({
                        'owner': owner,
                        'name': repo_name,
                        'full_name': f"{owner}/{repo_name}",
                        'url': url,
                        'link_text': text
                    })

        return repos

    def _get_repository_details(self, owner: str, repo: str) -> Optional[Dict]:
        """获取单个仓库的详细信息"""
        url = f"{Config.GITHUB_API_BASE}/repos/{owner}/{repo}"
        return self._make_request(url)

    def _search_repositories_by_topic(self, topic: str, sort: str = 'stars', per_page: int = 100) -> List[Dict]:
        """按主题搜索仓库"""
        repos = []
        url = f"{Config.GITHUB_API_BASE}/search/repositories"

        params = {
            'q': f'topic:{topic}',
            'sort': sort,
            'order': 'desc',
            'per_page': per_page
        }

        data = self._make_request(url, params)
        if data and 'items' in data:
            repos = data['items']

        return repos

    def crawl_awesome_list(self, awesome_repo: str = 'sindresorhus/awesome') -> int:
        """
        爬取 Awesome List 中的仓库
        这是主要的爬取方法
        """
        print(f"\n🔍 Starting Awesome List crawl from {awesome_repo}")

        # 获取 Awesome List 的 README
        url = f"{Config.GITHUB_API_BASE}/repos/{awesome_repo}/readme"
        readme_data = self._make_request(url)

        if not readme_data or 'content' not in readme_data:
            print("  [Error] Failed to fetch Awesome List README")
            return 0

        # 解析 base64 内容
        import base64
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')

        # 提取所有仓库链接
        repo_links = self._parseAwesome_list_readme(readme_content)
        print(f"  [Info] Found {len(repo_links)} repository links in Awesome List")

        # 限制爬取数量
        repo_links = repo_links[:Config.MAX_REPOS]
        print(f"  [Info] Limiting to top {Config.MAX_REPOS} repositories")

        # 爬取每个仓库的详细信息
        successful = 0
        failed = 0

        for i, repo_ref in enumerate(repo_links, 1):
            print(f"\n  [{i}/{len(repo_links)}] Fetching: {repo_ref['full_name']}")

            # 获取详细信息
            repo_details = self._get_repository_details(repo_ref['owner'], repo_ref['name'])

            if repo_details:
                # 添加 awesome_category 标记
                repo_details['awesome_category'] = awesome_repo

                # 保存到数据库
                if self.db.insert_repository(repo_details):
                    print(f"    ✓ Saved: {repo_details['full_name']} (⭐ {repo_details['stargazers_count']})")
                    successful += 1
                else:
                    print(f"    ✗ Failed to save: {repo_details['full_name']}")
                    failed += 1
            else:
                print(f"    ✗ Failed to fetch details")
                failed += 1

            # 延迟，避免触发速率限制
            if i < len(repo_links):
                time.sleep(Config.RATE_LIMIT_DELAY)

        # 记录爬取日志
        self.db.log_crawl(
            crawl_type='awesome_list',
            total=len(repo_links),
            successful=successful,
            failed=failed
        )

        print(f"\n✅ Crawl completed: {successful} successful, {failed} failed")
        return successful

    def crawl_trending_repos(self, language: str = None, since: str = 'weekly') -> int:
        """
        爬取 GitHub Trending 仓库
        language: 编程语言 (如 'python', 'javascript')
        since: 时间范围 ('daily', 'weekly', 'monthly')
        """
        print(f"\n🔥 Starting Trending crawl: {language or 'all languages'} ({since})")

        # 注意：GitHub API 不直接提供 Trending 接口，这里需要用 HTML 解析或搜索
        # 作为替代，使用搜索 API 按时间和 stars 排序

        url = f"{Config.GITHUB_API_BASE}/search/repositories"

        # 构建查询
        query = f'created:>{self._get_date_param(since)}'
        if language:
            query += f' language:{language}'

        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': Config.MAX_REPOS
        }

        data = self._make_request(url, params)

        if not data or 'items' not in data:
            print("  [Error] Failed to fetch trending repositories")
            return 0

        repos = data['items']
        print(f"  [Info] Found {len(repos)} trending repositories")

        successful = 0
        failed = 0

        for i, repo in enumerate(repos, 1):
            print(f"\n  [{i}/{len(repos)}] Processing: {repo['full_name']}")

            repo['awesome_category'] = f'trending_{since}'

            if self.db.insert_repository(repo):
                print(f"    ✓ Saved: {repo['full_name']} (⭐ {repo['stargazers_count']})")
                successful += 1
            else:
                print(f"    ✗ Failed to save: {repo['full_name']}")
                failed += 1

        # 记录日志
        self.db.log_crawl(
            crawl_type=f'trending_{since}',
            total=len(repos),
            successful=successful,
            failed=failed
        )

        print(f"\n✅ Trending crawl completed: {successful} successful, {failed} failed")
        return successful

    def _get_date_param(self, since: str) -> str:
        """获取日期参数"""
        from datetime import datetime, timedelta

        if since == 'daily':
            delta = timedelta(days=1)
        elif since == 'weekly':
            delta = timedelta(weeks=1)
        elif since == 'monthly':
            delta = timedelta(days=30)
        else:
            delta = timedelta(weeks=1)

        date = datetime.now() - delta
        return date.strftime('%Y-%m-%d')

    def crawl_by_language(self, language: str, limit: int = 100) -> int:
        """爬取指定语言的 Top 仓库"""
        print(f"\n📚 Starting language crawl: {language}")

        repos = self._search_repositories_by_topic(
            topic=language,
            sort='stars',
            per_page=limit
        )

        if not repos:
            print(f"  [Error] No repositories found for language: {language}")
            return 0

        print(f"  [Info] Found {len(repos)} repositories")

        successful = 0
        failed = 0

        for i, repo in enumerate(repos, 1):
            print(f"\n  [{i}/{len(repos)}] Processing: {repo['full_name']}")

            repo['awesome_category'] = f'language_{language}'

            if self.db.insert_repository(repo):
                print(f"    ✓ Saved: {repo['full_name']} (⭐ {repo['stargazers_count']})")
                successful += 1
            else:
                print(f"    ✗ Failed to save: {repo['full_name']}")
                failed += 1

        # 记录日志
        self.db.log_crawl(
            crawl_type=f'language_{language}',
            total=len(repos),
            successful=successful,
            failed=failed
        )

        print(f"\n✅ Language crawl completed: {successful} successful, {failed} failed")
        return successful


if __name__ == "__main__":
    # 测试爬虫
    crawler = GitHubCrawler()
    crawler.crawl_awesome_list()

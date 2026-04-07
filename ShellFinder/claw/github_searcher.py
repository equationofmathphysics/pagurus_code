"""
GitHub Searcher - 多线程GitHub搜索
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from dataclasses import dataclass
from config import Config


@dataclass
class SearchResult:
    """搜索结果"""
    name: str
    full_name: str
    description: str
    url: str
    stars: int
    language: str
    topics: List[str]
    query: str  # 触发此结果的搜索查询


class GitHubSearcher:
    """GitHub搜索器"""

    def __init__(self):
        """初始化搜索器"""
        self.api_base = Config.GITHUB_API_BASE
        self.token = Config.GITHUB_TOKEN
        self.headers = {}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.timeout = Config.SEARCH_TIMEOUT

        # 速率限制
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 最小请求间隔(秒)

    def _make_request(self, url: str, params: dict = None) -> dict:
        """
        发起API请求

        Args:
            url: 请求URL
            params: 查询参数

        Returns:
            响应JSON
        """
        # 速率限制
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time = time.time()

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            # 检查剩余配额
            remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
            if remaining != "unknown" and int(remaining) < 10:
                print(f"⚠️  API配额不足: 剩余 {remaining} 次")

            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise RuntimeError(
                    "❌ GitHub API速率限制!\n"
                    "请配置GitHub Token或稍后重试\n"
                    "获取Token: https://github.com/settings/tokens"
                )
            elif e.response.status_code == 422:
                return {"items": []}  # 无效查询，返回空结果
            else:
                raise RuntimeError(f"❌ API请求失败: {e}")
        except Exception as e:
            raise RuntimeError(f"❌ 请求异常: {e}")

    def search(self, query: str, per_page: int = None, sort: str = "stars") -> List[SearchResult]:
        """
        搜索GitHub仓库

        Args:
            query: 搜索查询
            per_page: 每页结果数
            sort: 排序方式 (stars, forks, updated)

        Returns:
            SearchResult列表
        """
        if per_page is None:
            per_page = Config.SEARCH_RESULTS_PER_MODULE

        url = f"{self.api_base}/search/repositories"
        params = {
            "q": query,
            "per_page": per_page,
            "sort": sort,
            "order": "desc"
        }

        print(f"🔍 搜索: {query}")

        data = self._make_request(url, params)
        items = data.get("items", [])

        results = []
        for item in items:
            result = SearchResult(
                name=item.get("name", ""),
                full_name=item.get("full_name", ""),
                description=item.get("description", ""),
                url=item.get("html_url", ""),
                stars=item.get("stargazers_count", 0),
                language=item.get("language", "Unknown"),
                topics=item.get("topics", []),
                query=query
            )
            results.append(result)

        print(f"   ✓ 找到 {len(results)} 个结果")
        return results

    def search_multiple(self, queries: List[str], max_workers: int = None) -> Dict[str, List[SearchResult]]:
        """
        并发搜索多个查询

        Args:
            queries: 搜索查询列表
            max_workers: 最大并发数

        Returns:
            查询 -> 结果列表的字典
        """
        if max_workers is None:
            max_workers = Config.MAX_CONCURRENT_SEARCHES

        results = {}

        print(f"\n🚀 开始并发搜索 ({len(queries)} 个查询, {max_workers} 并发)")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有搜索任务
            future_to_query = {
                executor.submit(self.search, query): query
                for query in queries
            }

            # 收集结果
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    search_results = future.result()
                    results[query] = search_results
                except Exception as e:
                    print(f"❌ 搜索失败 [{query}]: {e}")
                    results[query] = []

        return results

    def get_readme(self, owner: str, repo: str) -> str:
        """
        获取仓库的README内容

        Args:
            owner: 仓库所有者
            repo: 仓库名称

        Returns:
            README内容
        """
        url = f"{self.api_base}/repos/{owner}/{repo}/readme"
        data = self._make_request(url)

        # README内容是base64编码的
        import base64
        content = data.get("content", "")
        content = base64.b64decode(content).decode("utf-8")
        return content

    def search_by_module(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """
        为模块搜索相关仓库

        Args:
            module: 模块信息字典

        Returns:
            包含搜索结果的模块信息
        """
        module_name = module.get("name", "Unknown")
        print(f"\n📦 模块: {module_name}")

        # 获取搜索查询
        queries = module.get("github_search_queries", [])
        if not queries:
            keywords = module.get("search_keywords", [])
            queries = [f"{kw} template" for kw in keywords[:3]]

        # 并发搜索
        all_results = {}
        search_results = self.search_multiple(queries)

        # 按仓库去重 (相同仓库可能被多个查询命中)
        seen_repos = {}
        for query, results in search_results.items():
            for result in results:
                full_name = result.full_name
                if full_name not in seen_repos:
                    seen_repos[full_name] = result
                else:
                    # 更新查询记录
                    if query not in seen_repos[full_name].query:
                        seen_repos[full_name].query = f"{seen_repos[full_name].query}, {query}"

        # 转换为列表并排序
        unique_results = list(seen_repos.values())
        unique_results.sort(key=lambda x: x.stars, reverse=True)

        return {
            "module": module,
            "search_queries": queries,
            "results": [
                {
                    "name": r.name,
                    "full_name": r.full_name,
                    "description": r.description,
                    "url": r.url,
                    "stars": r.stars,
                    "language": r.language,
                    "topics": r.topics,
                    "matched_query": r.query
                }
                for r in unique_results[:Config.SEARCH_RESULTS_PER_MODULE]
            ],
            "total_found": len(unique_results)
        }


def test_searcher():
    """测试搜索器"""
    searcher = GitHubSearcher()

    # 测试单个搜索
    print("=== 测试单个搜索 ===")
    results = searcher.search("react admin template", per_page=5)
    for r in results:
        print(f"⭐ {r.stars} - {r.full_name}: {r.description[:50]}...")

    # 测试并发搜索
    print("\n=== 测试并发搜索 ===")
    queries = [
        "react admin template",
        "vue dashboard starter",
        "python api framework"
    ]
    results_dict = searcher.search_multiple(queries)

    for query, results in results_dict.items():
        print(f"\n{query}:")
        for r in results[:3]:
            print(f"  ⭐ {r.stars} - {r.full_name}")


if __name__ == "__main__":
    test_searcher()

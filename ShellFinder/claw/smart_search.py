"""
Smart Search - AI驱动的智能GitHub搜索
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from .analyzer import ArchitectureAnalyzer
from .github_searcher import GitHubSearcher
from config import Config


class SmartSearchOrchestrator:
    """智能搜索编排器"""

    def __init__(self):
        """初始化编排器"""
        self.analyzer = ArchitectureAnalyzer()
        self.searcher = GitHubSearcher()
        self.data_dir = Config.DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)

    def search_from_architecture(self, architecture_file: str) -> str:
        """
        从架构文件执行智能搜索

        Args:
            architecture_file: 架构文档路径

        Returns:
            结果文件路径
        """
        print("\n" + "="*60)
        print("🤖 AI智能搜索启动")
        print("="*60)

        # 1. 读取架构文档
        print(f"\n📄 读取架构文档: {architecture_file}")
        markdown_content = self._read_markdown(architecture_file)

        # 2. AI分析架构
        print("\n🧠 AI分析架构中...")
        try:
            analysis = self.analyzer.analyze_architecture(markdown_content)
            print("✅ 架构分析完成")
        except Exception as e:
            print(f"❌ 架构分析失败: {e}")
            raise

        # 3. 搜索每个模块
        print("\n🔍 搜索最佳项目模板...")
        modules = analysis.get("modules", [])
        module_results = []

        for i, module in enumerate(modules, 1):
            print(f"\n[{i}/{len(modules)}] 处理模块: {module.get('name')}")
            try:
                result = self.searcher.search_by_module(module)
                module_results.append(result)
            except Exception as e:
                print(f"❌ 模块搜索失败: {e}")
                module_results.append({
                    "module": module,
                    "error": str(e),
                    "results": []
                })

        # 4. 整合结果
        search_result = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "architecture_file": architecture_file,
                "total_modules": len(modules),
                "successful_searches": sum(1 for r in module_results if "error" not in r)
            },
            "analysis": analysis,
            "module_results": module_results
        }

        # 5. 保存结果
        output_file = self._save_results(search_result)

        # 6. 生成摘要
        self._print_summary(search_result)

        return output_file

    def _read_markdown(self, file_path: str) -> str:
        """读取Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"❌ 读取文件失败: {e}")

    def _save_results(self, result: Dict[str, Any]) -> str:
        """保存搜索结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"smart_search_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return filepath

    def _print_summary(self, result: Dict[str, Any]):
        """打印搜索摘要"""
        print("\n" + "="*60)
        print("📊 搜索结果摘要")
        print("="*60)

        analysis = result.get("analysis", {})
        print(f"\n🎯 项目概览: {analysis.get('project_overview', 'N/A')}")

        tech_stack = analysis.get("tech_stack", {})
        print("\n🛠️  技术栈:")
        for category, techs in tech_stack.items():
            if techs:
                print(f"   {category}: {', '.join(techs)}")

        module_results = result.get("module_results", [])
        print(f"\n📦 模块搜索结果:")

        total_repos = 0
        for module_result in module_results:
            if "error" in module_result:
                print(f"   ❌ {module_result['module'].get('name')}: 搜索失败")
                continue

            module = module_result["module"]
            results = module_result["results"]
            total_repos += len(results)

            print(f"   ✅ {module.get('name')}: {len(results)} 个候选项目")
            if results:
                top_result = results[0]
                print(f"      ⭐ 推荐: {top_result['full_name']} ({top_result['stars']} stars)")

        print(f"\n📈 总计: {total_repos} 个候选项目")

        metadata = result.get("metadata", {})
        print(f"\n💾 结果已保存到: {metadata.get('timestamp', '')}")

    def export_to_markdown(self, result_file: str, output_file: str = None) -> str:
        """
        将搜索结果导出为Markdown格式

        Args:
            result_file: JSON结果文件路径
            output_file: 输出Markdown文件路径

        Returns:
            输出文件路径
        """
        # 读取结果
        with open(result_file, 'r', encoding='utf-8') as f:
            result = json.load(f)

        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(
                self.data_dir,
                f"smart_search_report_{timestamp}.md"
            )

        # 生成Markdown
        md_content = self._generate_markdown(result)

        # 保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return output_file

    def _generate_markdown(self, result: Dict[str, Any]) -> str:
        """生成Markdown报告"""
        lines = []

        # 标题
        lines.append("# 🤖 智能搜索报告\n")
        lines.append(f"**生成时间**: {result['metadata']['timestamp']}\n")

        # 项目概览
        analysis = result.get("analysis", {})
        lines.append("## 📋 项目概览\n")
        lines.append(f"{analysis.get('project_overview', 'N/A')}\n")

        # 技术栈
        lines.append("## 🛠️ 技术栈\n")
        tech_stack = analysis.get("tech_stack", {})
        for category, techs in tech_stack.items():
            if techs:
                lines.append(f"- **{category}**: {', '.join(techs)}")
        lines.append("")

        # 模块搜索结果
        lines.append("## 📦 模块搜索结果\n")
        module_results = result.get("module_results", [])

        for module_result in module_results:
            if "error" in module_result:
                lines.append(f"### ❌ {module_result['module'].get('name')}\n")
                lines.append(f"搜索失败: {module_result['error']}\n")
                continue

            module = module_result["module"]
            results = module_result["results"]

            lines.append(f"### ✅ {module.get('name')}\n")
            lines.append(f"{module.get('description', 'N/A')}\n")

            if results:
                lines.append("**推荐项目**:\n\n")
                for i, repo in enumerate(results[:5], 1):
                    lines.append(f"{i}. **{repo['full_name']}** ⭐ {repo['stars']}")
                    lines.append(f"   - 描述: {repo['description'] or 'N/A'}")
                    lines.append(f"   - 语言: {repo['language']}")
                    lines.append(f"   - 链接: {repo['url']}")
                    if repo.get('topics'):
                        lines.append(f"   - 标签: {', '.join(repo['topics'])}")
                    lines.append("")

            lines.append("---\n")

        return "\n".join(lines)


def main():
    """测试"""
    orchestrator = SmartSearchOrchestrator()

    # 创建测试架构文件
    test_architecture = os.path.join(orchestrator.data_dir, "test_architecture.md")
    with open(test_architecture, 'w', encoding='utf-8') as f:
        f.write("""# 电商平台架构

## 技术栈
- 前端：React + TypeScript
- 后端：Python + FastAPI
- 数据库：PostgreSQL + Redis

## 功能模块

### 用户管理
用户注册、登录、JWT认证

### 商品管理
商品CRUD、分类管理

### 订单处理
订单创建、支付集成
""")

    # 执行搜索
    result_file = orchestrator.search_from_architecture(test_architecture)
    print(f"\n✅ 结果已保存到: {result_file}")

    # 导出Markdown
    md_file = orchestrator.export_to_markdown(result_file)
    print(f"✅ Markdown报告已保存到: {md_file}")


if __name__ == "__main__":
    main()

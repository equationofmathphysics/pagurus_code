#!/usr/bin/env python3
"""
ShellFinder - PaGURUS 模板仓库爬取与可视化工具

Usage:
    python shellfinder.py claw awesome       # 爬取 Awesome List
    python shellfinder.py claw trending      # 爬取 Trending
    python shellfinder.py smart arch.md      # AI智能搜索
    python shellfinder.py vis report         # 生成可视化报告
    python shellfinder.py vis list           # 列出所有数据集
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claw import GitHubCrawler, Database
from claw.smart_search import SmartSearchOrchestrator
from config import Config


def get_db_path(db_name: str = None, create_new: bool = False) -> str:
    """获取数据库路径"""
    if db_name:
        # 如果是完整路径
        if os.path.isabs(db_name):
            return db_name
        # 如果是文件名，在 data 目录中查找
        db_path = os.path.join(Config.DATA_DIR, db_name)
        if os.path.exists(db_path):
            return db_path
        # 如果不存在，尝试添加 .db 后缀
        if not db_name.endswith('.db'):
            db_path = os.path.join(Config.DATA_DIR, f"{db_name}.db")
            if os.path.exists(db_path):
                return db_path
        return db_path

    if create_new:
        # 创建新的按时间命名的数据库
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(Config.DATA_DIR, f"{timestamp}.db")

    # 使用最新的数据库
    if os.path.exists(Config.DATA_DIR):
        db_files = sorted([f for f in os.listdir(Config.DATA_DIR) if f.endswith('.db')], reverse=True)
        if db_files:
            return os.path.join(Config.DATA_DIR, db_files[0])

    # 如果没有数据库，创建新的
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(Config.DATA_DIR, f"{timestamp}.db")


def list_datasets():
    """列出所有数据集"""
    data_dir = Config.DATA_DIR
    if not os.path.exists(data_dir):
        print("📭 data 目录不存在")
        return

    db_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.db')], reverse=True)

    if not db_files:
        print("📭 data 目录中没有数据集")
        print("\n💡 提示: 先运行爬虫生成数据")
        print("   python shellfinder.py claw awesome")
        return

    print(f"\n📊 找到 {len(db_files)} 个数据集:\n")

    for i, db_file in enumerate(db_files, 1):
        db_path = os.path.join(data_dir, db_file)
        size_mb = os.path.getsize(db_path) / (1024 * 1024)

        # 从文件名提取时间
        timestamp = db_file.replace('.db', '')
        try:
            dt = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            time_str = timestamp

        # 获取数据库中的仓库数量
        try:
            db = Database(db_path)
            stats = db.get_statistics()
            repo_count = stats.get('total_repos', 0)
            print(f"  [{i}] {db_file}")
            print(f"      时间: {time_str}")
            print(f"      大小: {size_mb:.2f} MB")
            print(f"      仓库: {repo_count} 个")
            print()
        except Exception as e:
            print(f"  [{i}] {db_file}")
            print(f"      ⚠️  无法读取: {e}\n")


def run_crawl(args):
    """运行爬虫"""
    db_path = get_db_path(args.db, create_new=True)

    print(f"\n🔍 ShellFinder Crawler")
    print(f"=" * 50)
    print(f"数据库: {db_path}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 确保目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 设置数据库路径
    Config.DB_PATH = db_path

    # 创建爬虫实例
    crawler = GitHubCrawler()

    # 根据命令爬取
    if args.mode == 'awesome':
        count = crawler.crawl_awesome_list()
    elif args.mode == 'trending':
        count = crawler.crawl_trending_repos(language=args.lang)
    elif args.mode == 'lang':
        if not args.lang:
            print("❌ 错误: 使用 --lang 参数时需要指定语言")
            return
        count = crawler.crawl_by_language(args.lang)
    else:
        print(f"❌ 错误: 未知的爬取模式 '{args.mode}'")
        return

    print(f"\n✅ 爬取完成!")
    print(f"成功保存: {count} 个仓库")
    print(f"数据库位置: {db_path}")


def run_vis(args):
    """运行可视化"""
    db_path = get_db_path(args.db)

    if not os.path.exists(db_path):
        print(f"❌ 错误: 数据库不存在: {db_path}")
        print("\n💡 可用的数据集:")
        list_datasets()
        return

    print(f"\n📊 ShellFinder Visualization")
    print(f"=" * 50)
    print(f"数据库: {db_path}")
    print()

    # 设置数据库路径
    Config.DB_PATH = db_path

    if args.mode == 'report':
        # 生成 HTML 报告
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vis'))
        from report import generate_html_report

        # 如果用户指定了输出文件名，使用它；否则使用默认（数据库同目录）
        output = generate_html_report(args.output, db_path)

        print(f"\n✅ 报告已生成: {output}")
        print(f"💡 在浏览器中打开该文件查看")

    elif args.mode == 'app':
        # 启动 Streamlit 应用
        try:
            import subprocess
            app_path = os.path.join(os.path.dirname(__file__), 'vis', 'app.py')
            subprocess.run(['streamlit', 'run', app_path, '--server.headless', 'true'])
        except ImportError:
            print("❌ 错误: 未安装 streamlit")
            print("💡 安装: pip install streamlit plotly pandas")


def run_smart_search(args):
    """运行AI智能搜索"""
    architecture_file = args.architecture

    if not os.path.exists(architecture_file):
        print(f"❌ 错误: 架构文件不存在: {architecture_file}")
        return

    print(f"\n🤖 ShellFinder AI智能搜索")
    print(f"=" * 50)
    print(f"架构文件: {architecture_file}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        orchestrator = SmartSearchOrchestrator()
        result_file = orchestrator.search_from_architecture(architecture_file)

        print(f"\n✅ 智能搜索完成!")
        print(f"结果文件: {result_file}")

        # 如果用户要求导出Markdown
        if args.export_markdown:
            md_file = orchestrator.export_to_markdown(result_file)
            print(f"Markdown报告: {md_file}")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description='ShellFinder - PaGURUS 模板仓库爬取与可视化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 爬虫命令
    claw_parser = subparsers.add_parser('claw', help='爬取数据')
    claw_parser.add_argument(
        'mode',
        choices=['awesome', 'trending', 'lang'],
        help='爬取模式'
    )
    claw_parser.add_argument('--lang', help='编程语言（用于 lang 模式）')
    claw_parser.add_argument('--db', help='指定数据库文件名')

    # 智能搜索命令
    smart_parser = subparsers.add_parser('smart', help='AI智能搜索')
    smart_parser.add_argument(
        'architecture',
        help='架构文档路径 (Markdown格式)'
    )
    smart_parser.add_argument(
        '--export-markdown',
        '-m',
        action='store_true',
        help='同时导出Markdown格式报告'
    )

    # 可视化命令
    vis_parser = subparsers.add_parser('vis', help='可视化数据')
    vis_parser.add_argument(
        'mode',
        choices=['report', 'app', 'list'],
        help='可视化模式'
    )
    vis_parser.add_argument('--db', help='指定数据库文件名（默认使用最新）')
    vis_parser.add_argument('--output', '-o', help='输出文件名（用于 report 模式）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 显示欢迎信息
    print("""
    ╔═══════════════════════════════════════════╗
    ║       🦀 ShellFinder                    ║
    ║   PaGURUS 模板仓库爬取与可视化工具        ║
    ╚═══════════════════════════════════════════╝
    """)

    try:
        if args.command == 'claw':
            run_crawl(args)
        elif args.command == 'smart':
            run_smart_search(args)
        elif args.command == 'vis':
            if args.mode == 'list':
                list_datasets()
            else:
                run_vis(args)

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

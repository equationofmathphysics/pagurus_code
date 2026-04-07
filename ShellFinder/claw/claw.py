#!/usr/bin/env python3
"""
ShellFinder - PaGURUS Template Repository Crawler
主入口脚本

Usage:
    python main.py                    # 爬取 Awesome List
    python main.py --trending         # 爬取 Trending 仓库
    python main.py --lang python      # 爬取指定语言
    python main.py --report           # 生成数据质量报告
    python main.py --export           # 导出数据到 JSON
"""

import argparse
import sys
from datetime import datetime

from crawler import GitHubCrawler
from parser import DataParser
from database import Database
from config import Config


def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║           🦀 ShellFinder - PaGURUS Module            ║
    ║        Template Repository Crawler & Parser          ║
    ║                                                       ║
    ║  Clone -> Build -> Tweak                             ║
    ║  站在开源的肩膀上进行增量开发                          ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def run_crawl(mode: str = 'awesome', language: str = None):
    """执行爬取任务"""
    print(f"\n🚀 Starting crawl task: {mode}")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    crawler = GitHubCrawler()

    if mode == 'awesome':
        count = crawler.crawl_awesome_list()
    elif mode == 'trending':
        count = crawler.crawl_trending_repos(language=language)
    elif mode == 'language':
        if not language:
            print("❌ Error: --lang parameter required for language crawl")
            return False
        count = crawler.crawl_by_language(language)
    else:
        print(f"❌ Error: Unknown crawl mode '{mode}'")
        return False

    print(f"\n✅ Crawl completed: {count} repositories saved")
    print(f"⏰ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True


def generate_report():
    """生成数据质量报告"""
    print("\n📊 Generating data quality report...")

    parser = DataParser()
    report = parser.get_quality_report()

    print("\n" + "=" * 60)
    print("📊 SHELLFINDER DATA QUALITY REPORT")
    print("=" * 60)

    print("\n📈 Summary:")
    print("-" * 40)
    for key, value in report['summary'].items():
        print(f"  {key}: {value}")

    print("\n🎯 Quality Metrics:")
    print("-" * 40)
    for key, value in report['quality_metrics'].items():
        print(f"  {key}: {value}")

    print("\n💡 Recommendations:")
    print("-" * 40)
    if report['recommendations']:
        for rec in report['recommendations']:
            print(f"  {rec}")
    else:
        print("  ✅ Data quality looks good!")

    print("\n" + "=" * 60)

    # 显示最新的爬取日志
    db = Database()
    latest_log = db.get_latest_crawl_log()
    if latest_log:
        print(f"\n📝 Latest Crawl Log:")
        print(f"  Type: {latest_log['crawl_type']}")
        print(f"  Time: {latest_log['start_time']}")
        print(f"  Total: {latest_log['total_repos']}")
        print(f"  Successful: {latest_log['successful_repos']}")
        print(f"  Failed: {latest_log['failed_repos']}")


def export_data(output_path: str = None):
    """导出数据到 JSON"""
    if not output_path:
        output_path = f"shellfinder_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    print(f"\n📦 Exporting data to {output_path}...")

    parser = DataParser()
    success = parser.export_to_json(output_path)

    if success:
        print(f"✅ Export completed successfully")
    else:
        print(f"❌ Export failed")


def show_stats():
    """显示数据库统计信息"""
    print("\n📊 Database Statistics:")

    db = Database()
    stats = db.get_statistics()

    print(f"\n  Total Repositories: {stats['total_repos']}")
    print(f"  Average Stars: {stats['avg_stars']}")
    print(f"  Quality Rate: {stats['quality_rate']}%")

    print(f"\n  Top Languages:")
    for lang, count in list(stats['by_language'].items())[:10]:
        print(f"    {lang}: {count}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='ShellFinder - PaGURUS Template Repository Crawler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Crawl Awesome List (default)
  python main.py --trending         # Crawl trending repos
  python main.py --lang python      # Crawl Python repos
  python main.py --lang javascript  # Crawl JavaScript repos
  python main.py --report           # Generate quality report
  python main.py --export           # Export to JSON
  python main.py --stats            # Show statistics
        """
    )

    parser.add_argument(
        '--awesome',
        action='store_true',
        help='Crawl Awesome List repositories (default)'
    )

    parser.add_argument(
        '--trending',
        action='store_true',
        help='Crawl GitHub Trending repositories'
    )

    parser.add_argument(
        '--lang', '--language',
        type=str,
        help='Crawl repositories by programming language'
    )

    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate data quality report'
    )

    parser.add_argument(
        '--export',
        action='store_true',
        help='Export database to JSON file'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show database statistics'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path for export'
    )

    args = parser.parse_args()

    # 打印横幅
    print_banner()

    # 检查配置
    if not Config.GITHUB_TOKEN:
        print("\n⚠️  Warning: No GitHub token found in .env file")
        print("   Rate limit will be restricted (60 requests/hour)")
        print("   Get your token from: https://github.com/settings/tokens")
        print("   Add it to .env file: GITHUB_TOKEN=your_token_here\n")

    # 执行相应命令
    try:
        if args.report:
            generate_report()
        elif args.export:
            export_data(args.output)
        elif args.stats:
            show_stats()
        elif args.trending:
            run_crawl('trending', args.lang)
        elif args.lang:
            run_crawl('language', args.lang)
        else:
            # 默认行为：爬取 Awesome List
            run_crawl('awesome')

    except KeyboardInterrupt:
        print("\n\n⚠️  Task interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
ShellFinder Parser Module
解析模块 - 负责数据解析和质量验证
"""

import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import Counter

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from claw.database import Database


class DataParser:
    """数据解析和质量验证类"""

    def __init__(self):
        """初始化解析器"""
        self.db = Database()

    def validate_repository(self, repo_data: Dict) -> Tuple[bool, List[str]]:
        """
        验证仓库数据质量
        返回: (是否通过, 问题列表)
        """
        issues = []

        # 检查必填字段
        required_fields = ['id', 'name', 'full_name', 'html_url']
        for field in required_fields:
            if field not in repo_data or not repo_data[field]:
                issues.append(f"Missing required field: {field}")

        # 检查描述长度
        description = repo_data.get('description', '')
        if len(description) < Config.MIN_DESCRIPTION_LENGTH:
            issues.append(f"Description too short: {len(description)} < {Config.MIN_DESCRIPTION_LENGTH}")

        # 检查 stars 数量
        stars = repo_data.get('stargazers_count', 0)
        if stars < Config.MIN_STARS:
            issues.append(f"Stars below threshold: {stars} < {Config.MIN_STARS}")

        # 检查是否有 README
        if not repo_data.get('has_readme', True):
            issues.append("No README file found")

        # 检查最后更新时间
        updated_at = repo_data.get('updated_at')
        if updated_at:
            try:
                updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                days_since_update = (datetime.now(updated_date.tzinfo) - updated_date).days
                if days_since_update > 365:
                    issues.append(f"Repository not updated for {days_since_update} days")
            except:
                issues.append("Invalid updated_at format")

        # 检查语言
        if not repo_data.get('language'):
            issues.append("No programming language specified")

        is_valid = len(issues) == 0
        return is_valid, issues

    def analyze_repository(self, repo_data: Dict) -> Dict:
        """
        分析仓库数据，提取关键特征
        用于后续的模板匹配和检索
        """
        analysis = {
            'github_id': repo_data.get('id'),
            'name': repo_data.get('name'),
            'full_name': repo_data.get('full_name'),
            'language': repo_data.get('language'),
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'description': repo_data.get('description', ''),
            'topics': repo_data.get('topics', []),
            'license': repo_data.get('license', {}).get('name') if repo_data.get('license') else None,
            'has_wiki': repo_data.get('has_wiki', False),
            'has_pages': repo_data.get('has_pages', False),
            'has_issues': repo_data.get('has_issues', False),
            'is_template': repo_data.get('is_template', False),
            'archived': repo_data.get('archived', False),
            'size_kb': repo_data.get('size', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'subscribers_count': repo_data.get('subscribers_count', 0),
            'created_at': repo_data.get('created_at'),
            'updated_at': repo_data.get('updated_at'),
            'pushed_at': repo_data.get('pushed_at'),

            # 派生指标
            'fork_to_star_ratio': 0,
            'issue_to_star_ratio': 0,
            'activity_score': 0,
        }

        # 计算派生指标
        stars = analysis['stars']
        if stars > 0:
            analysis['fork_to_star_ratio'] = round(analysis['forks'] / stars, 3)
            analysis['issue_to_star_ratio'] = round(analysis['open_issues'] / stars, 3)

        # 计算活跃度得分 (综合考虑 stars, forks, recent updates)
        analysis['activity_score'] = self._calculate_activity_score(repo_data)

        return analysis

    def _calculate_activity_score(self, repo_data: Dict) -> float:
        """
        计算仓库活跃度得分
        综合考虑 stars, forks, 最近更新时间
        """
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        open_issues = repo_data.get('open_issues_count', 0)

        # 基础分：stars 和 forks
        base_score = stars + (forks * 2)

        # 活跃度加成：最近的更新和 issues
        pushed_at = repo_data.get('pushed_at')
        if pushed_at:
            try:
                pushed_date = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))
                days_since_push = (datetime.now(pushed_date.tzinfo) - pushed_date).days

                # 最近 30 天有更新，加成
                if days_since_push <= 30:
                    base_score *= 1.5
                # 最近 90 天有更新，小幅加成
                elif days_since_push <= 90:
                    base_score *= 1.2

            except:
                pass

        # Issues 反映社区活跃度
        base_score += open_issues * 0.5

        return round(base_score, 2)

    def extract_tech_stack(self, repo_data: Dict) -> List[str]:
        """
        从仓库数据中提取技术栈信息
        用于后续的模板匹配
        """
        tech_stack = []

        # 主要语言
        language = repo_data.get('language')
        if language:
            tech_stack.append(language.lower())

        # Topics
        topics = repo_data.get('topics', [])
        tech_stack.extend([t.lower() for t in topics])

        # 从描述中提取关键词
        description = repo_data.get('description', '').lower()

        # 常见技术栈关键词
        tech_keywords = [
            'react', 'vue', 'angular', 'svelte',
            'node', 'express', 'fastapi', 'django', 'flask',
            'mongodb', 'postgresql', 'mysql', 'redis',
            'docker', 'kubernetes', 'aws', 'azure',
            'tensorflow', 'pytorch', 'scikit-learn',
            'graphql', 'grpc', 'rest', 'api'
        ]

        for keyword in tech_keywords:
            if keyword in description and keyword not in tech_stack:
                tech_stack.append(keyword)

        return list(set(tech_stack))  # 去重

    def get_quality_report(self) -> Dict:
        """
        生成数据库质量报告
        """
        stats = self.db.get_statistics()

        report = {
            'summary': {
                'total_repositories': stats['total_repos'],
                'average_stars': stats['avg_stars'],
                'quality_rate': stats['quality_rate'],
                'by_language': stats['by_language']
            },
            'quality_metrics': self._calculate_quality_metrics(),
            'recommendations': self._generate_recommendations(stats)
        }

        return report

    def _calculate_quality_metrics(self) -> Dict:
        """计算详细的质量指标"""
        conn = self.db._get_connection()
        cursor = conn.cursor()

        metrics = {}

        # 平均描述长度
        cursor.execute("SELECT AVG(length(description)) as avg_desc FROM repositories")
        metrics['avg_description_length'] = round(cursor.fetchone()['avg_desc'] or 0, 2)

        # 有 README 的比例（通过描述长度来估算）
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN description IS NOT NULL AND length(description) > 10 THEN 1 ELSE 0 END) as with_readme
            FROM repositories
        """)
        row = cursor.fetchone()
        if row['total'] > 0:
            metrics['readme_rate'] = round(row['with_readme'] / row['total'] * 100, 2)
        else:
            metrics['readme_rate'] = 0

        # 有 topics 的比例
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN topics IS NOT NULL AND topics != '[]' THEN 1 ELSE 0 END) as with_topics
            FROM repositories
        """)
        row = cursor.fetchone()
        if row['total'] > 0:
            metrics['topics_rate'] = round(row['with_topics'] / row['total'] * 100, 2)
        else:
            metrics['topics_rate'] = 0

        # 活跃仓库比例（30 天内有更新）
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN updated_at > datetime('now', '-30 days') THEN 1 ELSE 0 END) as active
            FROM repositories
        """)
        row = cursor.fetchone()
        if row['total'] > 0:
            metrics['active_rate_30d'] = round(row['active'] / row['total'] * 100, 2)
        else:
            metrics['active_rate_30d'] = 0

        conn.close()
        return metrics

    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """根据统计数据生成改进建议"""
        recommendations = []

        if stats['total_repos'] < 50:
            recommendations.append("📈 仓库数量较少，建议增加爬取数量或扩大爬取范围")

        if stats['avg_stars'] < 1000:
            recommendations.append("⭐ 平均 star 数较低，考虑提高质量筛选阈值")

        if stats['quality_rate'] < 80:
            recommendations.append("📝 数据质量不高，建议增加描述长度和完整性要求")

        if not stats['by_language']:
            recommendations.append("🔍 缺少语言分类，建议按语言爬取特定技术栈的模板")

        return recommendations

    def export_to_json(self, output_path: str = 'shellfinder_export.json') -> bool:
        """
        导出数据库到 JSON 文件
        """
        try:
            repos = self.db.get_top_repositories(limit=1000)

            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_repos': len(repos),
                'repositories': repos
            }

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Exported {len(repos)} repositories to {output_path}")
            return True

        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False


if __name__ == "__main__":
    # 测试解析器
    parser = DataParser()

    # 生成质量报告
    report = parser.get_quality_report()

    print("\n📊 ShellFinder Data Quality Report")
    print("=" * 50)

    print("\n📈 Summary:")
    for key, value in report['summary'].items():
        print(f"  {key}: {value}")

    print("\n🎯 Quality Metrics:")
    for key, value in report['quality_metrics'].items():
        print(f"  {key}: {value}")

    print("\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"  {rec}")

    # 导出数据
    parser.export_to_json()

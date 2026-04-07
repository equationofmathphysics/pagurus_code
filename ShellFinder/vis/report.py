#!/usr/bin/env python3
"""
ShellFinder 静态 HTML 报告生成器
无需额外依赖，生成可在浏览器中直接查看的 HTML 报告
"""

import json
from datetime import datetime
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claw.database import Database
from claw.parser import DataParser
from config import Config


def generate_html_report(output_path: str = None, db_path: str = None):
    """生成 HTML 报告"""

    if db_path:
        Config.DB_PATH = db_path

    db = Database()

    # 如果没有指定输出路径，使用数据库同目录
    if output_path is None:
        db_dir = os.path.dirname(db.db_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(db_dir, f"shellfinder_report_{timestamp}.html")
    # 如果是相对路径，也使用数据库同目录
    elif not os.path.isabs(output_path):
        db_dir = os.path.dirname(db.db_path)
        output_path = os.path.join(db_dir, output_path)

    parser = DataParser()

    # 获取数据
    conn = db._get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM repositories ORDER BY stars DESC")
    repos = [dict(row) for row in cursor.fetchall()]

    stats = db.get_statistics()
    report = parser.get_quality_report()

    conn.close()

    # 生成 HTML
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦀 ShellFinder Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #6c757d; margin-top: 5px; }}
        .section {{
            padding: 40px;
            border-bottom: 1px solid #e9ecef;
        }}
        .section h2 {{
            color: #495057;
            margin-bottom: 25px;
            font-size: 1.8em;
        }}
        .repo-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .repo-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        .repo-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        .repo-table tr:hover {{ background: #f8f9fa; }}
        .repo-name {{ font-weight: 600; color: #667eea; }}
        .language-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        .stars {{ color: #ffc107; }}
        .chart-container {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
        }}
        .bar {{
            height: 30px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 15px;
            margin: 10px 0;
            position: relative;
            transition: width 0.5s ease;
        }}
        .bar-label {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: 600;
        }}
        .bar-value {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: 600;
        }}
        .quality-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .quality-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .quality-label {{ color: #6c757d; font-size: 0.9em; }}
        .quality-value {{ font-size: 1.8em; font-weight: bold; color: #495057; }}
        .footer {{
            background: #343a40;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .recommendation {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦀 ShellFinder 数据报告</h1>
            <p>PaGURUS 模板仓库爬取与分析报告</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(repos)}</div>
                <div class="stat-label">📦 总仓库数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['avg_stars']:.0f}</div>
                <div class="stat-label">⭐ 平均 Stars</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['quality_rate']}%</div>
                <div class="stat-label">✨ 质量达标率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['by_language'])}</div>
                <div class="stat-label">💻 覆盖语言</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 质量指标</h2>
            <div class="quality-metrics">
                <div class="quality-item">
                    <div class="quality-label">平均描述长度</div>
                    <div class="quality-value">{report['quality_metrics']['avg_description_length']} 字符</div>
                </div>
                <div class="quality-item">
                    <div class="quality-label">README 覆盖率</div>
                    <div class="quality-value">{report['quality_metrics']['readme_rate']}%</div>
                </div>
                <div class="quality-item">
                    <div class="quality-label">活跃仓库 (30天)</div>
                    <div class="quality-value">{report['quality_metrics']['active_rate_30d']}%</div>
                </div>
                <div class="quality-item">
                    <div class="quality-label">Topics 标注率</div>
                    <div class="quality-value">{report['quality_metrics']['topics_rate']}%</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>💻 编程语言分布</h2>
            <div class="chart-container">
"""

    # 添加语言分布图表
    lang_stats = stats['by_language']
    max_count = max(lang_stats.values()) if lang_stats else 1

    for lang, count in list(lang_stats.items())[:10]:
        width = (count / max_count) * 100
        html += f"""
                <div class="bar" style="width: {width}%">
                    <span class="bar-label">{lang}</span>
                    <span class="bar-value">{count}</span>
                </div>
"""

    html += """
            </div>
        </div>

        <div class="section">
            <h2>🏆 Top 50 仓库</h2>
            <table class="repo-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>仓库名称</th>
                        <th>语言</th>
                        <th>⭐ Stars</th>
                        <th>🍴 Forks</th>
                        <th>描述</th>
                    </tr>
                </thead>
                <tbody>
"""

    # 添加 Top 50 仓库表格
    for idx, repo in enumerate(repos[:50], 1):
        html += f"""
                    <tr>
                        <td>#{idx}</td>
                        <td><a href="{repo['url']}" target="_blank" class="repo-name">{repo['full_name']}</a></td>
                        <td><span class="language-tag" style="background: #{hash(repo['language'] or 'unknown') % 0xFFFFFF:06x}; color: white;">{repo['language'] or 'N/A'}</span></td>
                        <td class="stars">⭐ {repo['stars']:,}</td>
                        <td>🍴 {repo['forks']:,}</td>
                        <td style="max-width: 400px;">{repo['description'] or '无描述'}</td>
                    </tr>
"""

    html += """
                </tbody>
            </table>
        </div>
"""

    # 添加改进建议
    if report['recommendations']:
        html += """
        <div class="section">
            <h2>💡 改进建议</h2>
"""
        for rec in report['recommendations']:
            html += f"""
            <div class="recommendation">{rec}</div>
"""
        html += """
        </div>
"""

    # 页脚
    html += f"""
        <div class="footer">
            <p>🦀 PaGURUS - ShellFinder Module</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
            <p style="margin-top: 5px; opacity: 0.6; font-size: 0.9em;">
                Template is Quality, Execution is Truth
            </p>
        </div>
    </div>
</body>
</html>
"""

    # 保存 HTML 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML 报告已生成: {output_path}")
    print(f"📊 总仓库数: {len(repos)}")
    print(f"⭐ 平均 Stars: {stats['avg_stars']:.0f}")
    print(f"✨ 质量率: {stats['quality_rate']}%")
    print(f"\n💡 在浏览器中打开报告查看详细内容")

    return output_path


if __name__ == "__main__":
    generate_html_report()

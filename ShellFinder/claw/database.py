"""
ShellFinder Database Module
数据库模块 - 负责数据存储和检索
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import json

from config import Config


class Database:
    """数据库管理类"""

    def __init__(self, db_path: str = None):
        """初始化数据库"""
        self.db_path = db_path or Config.DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 创建 repositories 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                github_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                owner TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL,
                language TEXT,
                stars INTEGER DEFAULT 0,
                forks INTEGER DEFAULT 0,
                topics TEXT,
                awesome_category TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_data TEXT
            )
        """)

        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_github_id ON repositories(github_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_stars ON repositories(stars)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_language ON repositories(language)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_awesome_category ON repositories(awesome_category)
        """)

        # 创建 crawl_log 表（爬取日志）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crawl_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawl_type TEXT NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_repos INTEGER DEFAULT 0,
                successful_repos INTEGER DEFAULT 0,
                failed_repos INTEGER DEFAULT 0,
                error_message TEXT
            )
        """)

        conn.commit()
        conn.close()

    def insert_repository(self, repo_data: Dict) -> bool:
        """插入或更新仓库数据"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO repositories (
                    github_id, name, full_name, owner, description,
                    url, language, stars, forks, topics, awesome_category,
                    created_at, updated_at, raw_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                repo_data.get('id'),
                repo_data.get('name'),
                repo_data.get('full_name'),
                repo_data.get('owner', {}).get('login'),
                repo_data.get('description'),
                repo_data.get('html_url'),
                repo_data.get('language'),
                repo_data.get('stargazers_count', 0),
                repo_data.get('forks_count', 0),
                json.dumps(repo_data.get('topics', [])),
                repo_data.get('awesome_category'),
                repo_data.get('created_at'),
                repo_data.get('updated_at'),
                json.dumps(repo_data)
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"Error inserting repository {repo_data.get('full_name')}: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    def get_repository_by_github_id(self, github_id: int) -> Optional[Dict]:
        """根据 GitHub ID 获取仓库"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM repositories WHERE github_id = ?
        """, (github_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_top_repositories(self, limit: int = 100, language: str = None) -> List[Dict]:
        """获取 Top N 仓库（按 stars 排序）"""
        conn = self._get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM repositories WHERE stars >= ?"
        params = [Config.MIN_STARS]

        if language:
            query += " AND language = ?"
            params.append(language)

        query += " ORDER BY stars DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """获取数据库统计信息"""
        conn = self._get_connection()
        cursor = conn.cursor()

        stats = {}

        # 总仓库数
        cursor.execute("SELECT COUNT(*) as total FROM repositories")
        stats['total_repos'] = cursor.fetchone()['total']

        # 按语言统计
        cursor.execute("""
            SELECT language, COUNT(*) as count
            FROM repositories
            GROUP BY language
            ORDER BY count DESC
        """)
        stats['by_language'] = {row['language']: row['count'] for row in cursor.fetchall()}

        # Stars 统计
        cursor.execute("SELECT AVG(stars) as avg_stars FROM repositories")
        stats['avg_stars'] = round(cursor.fetchone()['avg_stars'], 2)

        # 质量指标（达到最低要求的仓库比例）
        cursor.execute(f"""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN length(description) >= {Config.MIN_DESCRIPTION_LENGTH} THEN 1 ELSE 0 END) as with_desc
            FROM repositories
        """)
        row = cursor.fetchone()
        if row['total'] > 0:
            stats['quality_rate'] = round(row['with_desc'] / row['total'] * 100, 2)
        else:
            stats['quality_rate'] = 0

        conn.close()
        return stats

    def log_crawl(self, crawl_type: str, total: int, successful: int, failed: int, error: str = None):
        """记录爬取日志"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO crawl_log (crawl_type, start_time, total_repos, successful_repos, failed_repos, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (crawl_type, datetime.now(), total, successful, failed, error))

        conn.commit()
        conn.close()

    def get_latest_crawl_log(self) -> Optional[Dict]:
        """获取最新的爬取日志"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM crawl_log ORDER BY id DESC LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None


if __name__ == "__main__":
    # 测试数据库
    db = Database()
    stats = db.get_statistics()
    print("Database Statistics:")
    print(f"Total Repositories: {stats['total_repos']}")
    print(f"Average Stars: {stats['avg_stars']}")
    print(f"Quality Rate: {stats['quality_rate']}%")
    print(f"\nBy Language: {stats['by_language']}")

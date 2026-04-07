"""
ShellFinder Configuration
配置文件
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """配置类"""

    # GitHub API Configuration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_API_BASE = "https://api.github.com"
    GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

    # Awesome List Source
    AWESOME_LIST_URL = f"{GITHUB_API_BASE}/repos/sindresorhus/awesome/readme"

    # Crawler Settings
    MAX_REPOS = 100  # Top 100 repositories
    REQUEST_TIMEOUT = 30
    RATE_LIMIT_DELAY = 1  # seconds between requests

    # Database
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    DB_PATH = os.getenv("DB_PATH", None)  # None = auto-generate by timestamp

    # Data Quality Thresholds
    MIN_STARS = 100  # Minimum stars to be considered
    MIN_DESCRIPTION_LENGTH = 20

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 支持国内大模型API
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS = 4000
    OPENAI_TEMPERATURE = 0.7

    # Smart Search Settings
    SEARCH_RESULTS_PER_MODULE = 10  # Number of GitHub results per module
    MAX_CONCURRENT_SEARCHES = 5  # Max concurrent GitHub API searches
    SEARCH_TIMEOUT = 30  # Timeout for each search request

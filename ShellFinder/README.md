# 🔍 ShellFinder

> **PaGURUS 模板仓库爬取与可视化工具** - 负责检索和爬取高质量的开源项目模板

## 📋 项目结构

```
ShellFinder/
├── claw/                # 爬虫模块
│   ├── crawler.py      # GitHub API 爬虫
│   ├── database.py     # 数据库操作
│   └── parser.py       # 数据解析和质量验证
├── vis/                # 可视化模块
│   ├── report.py       # HTML 报告生成
│   └── app.py          # Streamlit Web 应用
├── data/               # 数据存储（按时间分组）
│   └── 20260407_104226.db
├── shellfinder.py      # 主入口脚本
├── config.py           # 配置文件
└── requirements.txt    # Python 依赖
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

创建 `.env` 文件：

```env
GITHUB_TOKEN=your_github_token_here
```

> 获取 GitHub Token: https://github.com/settings/tokens

### 3. 使用命令

#### 📊 爬取数据

```bash
# 爬取 Awesome List
python shellfinder.py claw awesome

# 爬取 Trending 仓库
python shellfinder.py claw trending

# 爬取特定语言
python shellfinder.py claw lang --lang python

# 指定数据库名称
python shellfinder.py claw awesome --db my_data
```

#### 👁️ 可视化数据

```bash
# 查看所有数据集
python shellfinder.py vis list

# 生成 HTML 报告（使用最新数据集，保存到 data/ 目录）
python shellfinder.py vis report

# 使用指定数据集
python shellfinder.py vis report --db 20260407_104226

# 指定输出文件名（也保存到 data/ 目录）
python shellfinder.py vis report --output my_report.html
```

## 💾 数据管理

数据集按时间戳自动命名并存储在 `data/` 目录：

```
data/
├── 20260407_104226.db   # 2026-04-07 10:42:26 的数据
├── 20260407_151230.db   # 2026-04-07 15:12:30 的数据
└── ...
```

每次爬取都会创建新的数据库文件，保留历史数据。

## 📊 数据质量指标

系统自动检查：
- ⭐ 最低 Star 数（默认 ≥ 100）
- 📝 描述长度（默认 ≥ 20 字符）
- 🕐 最近更新时间
- 💻 编程语言标签

## 📈 示例输出

```
╔═══════════════════════════════════════════╗
║       🦀 ShellFinder                    ║
║   PaGURUS 模板仓库爬取与可视化工具        ║
╚═══════════════════════════════════════════╝

📊 找到 1 个数据集:

  [1] 20260407_104226.db
      时间: 2026-04-07 10:42:26
      大小: 0.79 MB
      仓库: 100 个
```

## 🎯 下一步

- [ ] 支持从 GitHub Topics 搜索
- [ ] 集成向量检索（Qdrant）
- [ ] 添加相似度计算和推荐
- [ ] Web UI 优化

## 📄 许可证

MIT License

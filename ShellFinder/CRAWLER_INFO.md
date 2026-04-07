# 🔍 ShellFinder 爬虫工作原理

## 📚 爬虫在爬什么？

ShellFinder 爬虫的核心逻辑：**从 Awesome List 中提取仓库列表，然后获取每个仓库的详细信息**

### 🎯 数据源：Awesome List

**Awesome List** 是 GitHub 上的一个精选项目列表仓库：
- 仓库：`sindresorhus/awesome`
- URL：https://github.com/sindresorhus/awesome
- 内容：按主题分类的精选开源项目列表

## 🔧 爬虫工作流程

```
1. 获取 Awesome List 的 README.md
   ↓
2. 从 README 中提取所有 GitHub 仓库链接
   ↓
3. 对每个仓库调用 GitHub API 获取详细信息
   ↓
4. 保存到数据库
```

### 📝 具体步骤

#### Step 1: 获取 Awesome List
```python
# GitHub API 获取 README
url = "https://api.github.com/repos/sindresorhus/awesome/readme"
```

#### Step 2: 解析 README 提取链接
使用正则表达式匹配 Markdown 链接：
```python
# 匹配 [text](https://github.com/owner/repo) 格式
pattern = r'\[([^\]]+)\]\((https://github\.com/[^/]+/[^)\s]+)\)'
```

#### Step 3: 获取每个仓库的详细信息
```python
# 对每个仓库调用 GitHub API
url = f"https://api.github.com/repos/{owner}/{repo}"
```

## 📊 爬取的数据字段

每个仓库保存以下信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| `github_id` | GitHub 仓库 ID | 1296269 |
| `name` | 仓库名称 | `awesome-nodejs` |
| `full_name` | 完整名称 | `sindresorhus/awesome-nodejs` |
| `owner` | 所有者 | `sindresorhus` |
| `description` | 描述 | "Delightful Node.js packages and resources" |
| `url` | 仓库 URL | `https://github.com/sindresorhus/awesome-nodejs` |
| `language` | 主要语言 | `Python`, `JavaScript` 等 |
| `stars` | Star 数量 | 65514 |
| `forks` | Fork 数量 | 5234 |
| `topics` | GitHub Topics | `nodejs`, `awesome`, `list` |
| `created_at` | 创建时间 | `2014-01-01T00:00:00Z` |
| `updated_at` | 更新时间 | `2026-04-01T00:00:00Z` |
| `raw_data` | 完整 JSON 响应 | ... |

## 🎯 实际爬取的内容示例

从你的数据中可以看到：

```json
{
  "full_name": "vsouza/awesome-ios",
  "language": "Swift",
  "stars": 51730,
  "description": "A curated list of awesome iOS ecosystem...",
  "url": "https://github.com/vsouza/awesome-ios"
}
```

## 🤔 问题与限制

### 当前存在的问题

1. **数据源局限**
   - 只爬取 Awesome List 中的链接
   - Awesome List 本身是一个"列表的列表"，包含很多 Awesome 系列仓库
   - **不是真正的独立项目模板**

2. **数据质量问题**
   - 很多仓库没有 `language` 字段（见示例数据）
   - 描述较短或不完整
   - 包含大量"Awesome"列表而非实际项目

3. **实用性问题**
   - 爬到的大多是"精选列表"而非"项目模板"
   - 对 PaGURUS 的"找壳"目标帮助有限

## 💡 改进建议

### 更好的爬取策略

1. **直接爬取模板项目**
   ```bash
   # 按技术栈搜索 starter/template 项目
   python shellfinder.py claw lang --lang python
   ```

2. **使用 GitHub 搜索 API**
   ```python
   # 搜索 "starter" 或 "template" 项目
   q = "starter template language:python"
   url = "https://api.github.com/search/repositories?q={q}"
   ```

3. **爬取知名模板库**
   - https://github.com/Azure-Samples (Azure 官方示例)
   - https://github.com/aws-samples (AWS 官方示例)
   - 各种 *-starter-* 仓库

4. **按技术栈爬取**
   ```bash
   # 爬取 Python 热门项目（更适合做模板）
   python shellfinder.py claw trending --lang python
   ```

## 🎯 总结

**当前爬虫爬取的是**：Awesome List 中列出的仓库链接

**问题是**：这些大多是"列表"而非"项目模板"

**建议**：
1. ✅ 使用 `--lang` 参数直接爬取编程语言的热门项目
2. ✅ 搜索包含 "starter" 或 "template" 关键词的仓库
3. ✅ 爬取官方示例库（Azure/AWS/Google Samples）

这样才能真正找到适合作为"壳"的项目模板！

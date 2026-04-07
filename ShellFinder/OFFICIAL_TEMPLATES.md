# 🏢 官方模板库详细说明

## ✅ 是的，这些都是 GitHub 组织！

Azure Samples、AWS Samples、Google Cloud Samples 都是各大云厂商在 **GitHub 上托管的官方示例仓库**。

---

## 📦 各大云厂商的官方示例库

### 1. Microsoft Azure Samples

**GitHub 组织**：[Azure-Samples](https://github.com/Azure-Samples)

**主要仓库**：
- [azure-samples](https://github.com/Azure-Samples/azure-samples) - 主仓库
- 包含 **2000+** 个示例项目

**典型项目示例**：
```
✅ azure-search-openai-demo-csharp       (AI + 搜索)
✅ functions-quickstart                  (Azure Functions 快速开始)
✅ appservice-mobile-quickstart          (移动应用后端)
✅ storage-blobs-dotnet-quickstart       (存储服务示例)
```

**特点**：
- 🎯 每个项目都是**完整可运行的**
- 📚 包含详细文档和部署指南
- 🔧 最佳实践参考实现
- 💻 覆盖多种语言：Python, C#, JavaScript, Java, Go

---

### 2. AWS Samples

**GitHub 组织**：[aws-samples](https://github.com/aws-samples)

**主要仓库**：
- [aws-samples](https://github.com/aws-samples) - 主组织页面
- 包含 **4000+** 个示例项目

**典型项目示例**：
```
✅ aws-serverless-airline-booking        (无服务器架构)
✅ ecs-demo-worker                       (容器编排)
✅ lambda-with-s3                        (函数计算)
✅ aws-cdk-examples                      (基础设施即代码)
```

**特点**：
- 🏗️ 完整的生产级架构示例
- 📖 详细的部署文档
- 🔐 安全最佳实践
- 💡 多种技术栈组合示例

---

### 3. Google Cloud Samples

**GitHub 组织**：[GoogleCloudPlatform](https://github.com/GoogleCloudPlatform)

**主要仓库**：
- [cloud-code-samples](https://github.com/GoogleCloudPlatform/cloud-code-samples)
- [python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
- [nodejs-docs-samples](https://github.com/GoogleCloudPlatform/nodejs-docs-samples)

**典型项目示例**：
```
✅ python-docs-samples/functions        (Cloud Functions)
✅ nodejs-docs-samples/appengine        (App Engine)
✅ cloud-code-samples/kubernetes        (K8s 示例)
```

**特点**：
- 🎓 教学友好
- 🔬 涵盖最新技术
- 📝 代码注释详细
- 🚀 快速开始模板

---

## 🎯 其他优质官方模板库

### 4. GitHub 官方模板

**GitHub 组织**：[github](https://github.com/github)

**主要仓库**：
```
✅ github/project-template              (GitHub 项目模板)
✅ github/semantic-git-flow             (Git 工作流)
✅ github/renaming                      (项目重命名工具)
```

### 5. Vue.js 官方

**GitHub 组织**：[vuejs](https://github.com/vuejs)

**模板仓库**：
```
✅ vuejs/create-vue                    (Vue 3 项目脚手架)
✅ vuejs/vue-hn                        (Hacker News 克隆)
```

### 6. React 官方

**GitHub 组织**：[facebook](https://github.com/facebook)

**模板仓库**：
```
✅ facebook/create-react-app           (React 脚手架)
✅ facebook/react-native               (React Native)
```

### 7. Next.js 官方

**GitHub 组织**：[vercel](https://github.com/vercel)

**模板仓库**：
```
✅ vercel/next.js                      (Next.js 框架)
✅ vercel/examples                     (各种使用案例)
```

### 8. Python 官方

**GitHub 组织**：[python](https://github.com/python)

**模板仓库**：
```
✅ python/cpython                      (Python 解释器)
✅ python/mypy                         (类型检查)
```

---

## 📊 这些模板的质量特点

| 特性 | 官方模板 | 普通开源项目 |
|------|---------|------------|
| ✅ 代码质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ✅ 文档完整性 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| ✅ 最佳实践 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ✅ 安全性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ✅ 维护更新 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ✅ 生产就绪 | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## 🎯 如何使用这些模板？

### 方法 1：直接在 GitHub 上搜索

```
site:github.com/Azure-Samples python
site:github.com/aws-samples javascript
site:github.com/GoogleCloudPlatform golang
```

### 方法 2：使用 GitHub API

```python
# 搜索 Azure Samples 的 Python 项目
url = "https://api.github.com/search/repositories"
params = {
    "q": "org:Azure-Samples language:python",
    "sort": "stars",
    "per_page": 100
}
```

### 方法 3：使用 ShellFinder（需要修改代码）

可以修改 ShellFinder 的爬虫，增加爬取官方组织的功能：

```python
# 在 crawler.py 中添加
def crawl_official_orgs(self, org: str, language: str = None):
    """爬取官方组织的仓库"""
    url = f"{Config.GITHUB_API_BASE}/orgs/{org}/repos"

    params = {
        "type": "public",
        "sort": "updated",
        "per_page": 100
    }

    repos = self._make_request(url, params)

    # 保存到数据库...
```

---

## 💡 推荐的爬取策略

### 优先级排序

1. **官方模板库** ⭐⭐⭐⭐⭐
   ```
   Azure-Samples
   aws-samples
   GoogleCloudPlatform
   ```

2. **知名框架官方** ⭐⭐⭐⭐
   ```
   vercel (Next.js)
   vuejs
   facebook (React)
   ```

3. **技术栈特定** ⭐⭐⭐
   ```
   按语言搜索 + "starter" 或 "template" 关键词
   ```

4. **社区精选** ⭐⭐
   ```
   Awesome List（当前在用的）
   ```

---

## 🚀 立即行动

如果你想爬取这些官方模板：

```bash
# 爬取 Azure Samples（需要先修改代码支持 org 参数）
# python shellfinder.py claw org --org Azure-Samples

# 或者直接访问它们的 GitHub 页面
# https://github.com/Azure-Samples
# https://github.com/aws-samples
# https://github.com/GoogleCloudPlatform
```

这些官方模板库才是真正适合 PaGURUS "找壳"需求的高质量项目模板！

# LLM 配置指南

## 支持的模型服务

ShellFinder 支持所有兼容 OpenAI API 格式的模型服务，包括：

### 🌍 国际服务

| 服务商 | Base URL | 推荐模型 | 获取地址 |
|--------|----------|----------|----------|
| **OpenAI** | `https://api.openai.com/v1` | `gpt-4o-mini` | [platform.openai.com](https://platform.openai.com/api-keys) |
| **DeepSeek** | `https://api.deepseek.com` | `deepseek-chat` | [platform.deepseek.com](https://platform.deepseek.com) |

### 🇨🇳 国内服务

| 服务商 | Base URL | 推荐模型 | 获取地址 |
|--------|----------|----------|----------|
| **阿里云通义千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo` | [dashscope.aliyuncs.com](https://dashscope.aliyuncs.com) |
| **智谱AI (GLM)** | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-flash` | [open.bigmodel.cn](https://open.bigmodel.cn) |
| **百度文心一言** | `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop` | `ERNIE-Bot-turbo` | [aip.baidubce.com](https://aip.baidubce.com) |

---

## 快速配置

### 方式一：OpenAI（国际）

```bash
# .env 文件
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### 方式二：阿里云通义千问（推荐国内用户）

```bash
# .env 文件
OPENAI_API_KEY=sk-your-qwen-key-here
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-turbo
```

### 方式三：智谱AI

```bash
# .env 文件
OPENAI_API_KEY=your-glm-key-here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
OPENAI_MODEL=glm-4-flash
```

### 方式四：DeepSeek

```bash
# .env 文件
OPENAI_API_KEY=sk-your-deepseek-key-here
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

---

## 获取 API Key

### OpenAI
1. 访问 [platform.openai.com](https://platform.openai.com)
2. 登录 → Settings → API keys
3. 创建新 Key

### 阿里云通义千问
1. 访问 [dashscope.aliyuncs.com](https://dashscope.aliyuncs.com)
2. 登录阿里云账号 → API-KEY管理
3. 创建 API Key

### 智谱AI
1. 访问 [open.bigmodel.cn](https://open.bigmodel.cn)
2. 注册/登录 → 右上角API密钥
3. 获取 API Key

### DeepSeek
1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
2. 注册/登录 → API Keys
3. 创建新 Key

---

## 模型选择建议

### 按成本选择（从低到高）

| 模型 | 服务商 | 特点 | 适用场景 |
|------|--------|------|----------|
| `glm-4-flash` | 智谱AI | 便宜、快速 | 测试、开发 |
| `qwen-turbo` | 阿里云 | 性价比高 | 日常使用 |
| `gpt-4o-mini` | OpenAI | 平衡性好 | 通用场景 |
| `deepseek-chat` | DeepSeek | 智能强 | 复杂分析 |
| `qwen-plus` | 阿里云 | 性能强 | 生产环境 |
| `glm-4-plus` | 智谱AI | 能力强 | 生产环境 |
| `gpt-4o` | OpenAI | 最强 | 高质量需求 |

---

## 测试配置

配置完成后，运行以下命令测试：

```bash
# 测试AI分析器
python -m ShellFinder.claw.analyzer

# 测试完整智能搜索
python shellfinder.py smart example_architecture.md
```

---

## 常见问题

### Q: 提示 "API Key未设置"？
**A**: 检查 `.env` 文件是否正确配置，确保 `OPENAI_API_KEY` 已填写

### Q: 国内访问 OpenAI 很慢？
**A**: 建议使用国内服务（通义千问、智谱AI等），速度更快

### Q: 如何切换模型？
**A**: 只需修改 `.env` 中的 `OPENAI_MODEL` 参数即可

### Q: API 请求失败？
**A**: 检查：
1. API Key 是否正确
2. Base URL 是否匹配
3. 账户是否有余额
4. 网络是否正常

---

## 推荐配置

**国内用户推荐**：
```bash
# 阿里云通义千问 - 速度快、价格低
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-turbo
```

**国际用户推荐**：
```bash
# OpenAI - 质量最高
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

**追求性价比**：
```bash
# DeepSeek - 当前最强且便宜
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

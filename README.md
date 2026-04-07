# 🦀 PaGURUS

> **Execution-Guided Repository-Level Code Agent**  
> **基于执行反馈与模板检索的仓库级代码智能体**
>
> *Clone, Build, and Tweak—Standing on the Shoulders of Open Source*  
> *克隆、构建、改造——站在开源的肩膀上*

---

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) 
[![中文](https://img.shields.io/badge/lang-中文-red.svg)](README.md)
![Status](https://img.shields.io/badge/status-concept-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 💡 What is PaGURUS? / 什么是 PaGURUS？

**[EN]** **PaGURUS** is a repository-level code agent that generates code by **finding, running, and modifying** existing open-source templates, rather than generating from scratch.

**[中文]** **PaGURUS** 是一个仓库级代码智能体，通过 **"找壳→钻壳→改壳"** 的方式，在现有开源项目基础上进行增量开发，而非从零开始生成。

---

## 🦭 Core Concept / 核心概念

**[EN]** Like a hermit crab that finds, occupies, and modifies shells, PaGURUS follows the **"Find Shell → Drill Shell → Modify Shell"** philosophy:

**[中文]** 就像寄居蟹寻找、钻入、改造壳一样，PaGURUS 遵循 **"找壳→钻壳→改壳"** 的理念：

| **[EN] Step** | **[中文] 步骤** |
|--------------|----------------|
| 🔍 **Find Shell** — Search and retrieve the best-matching open-source template | 🔍 **找壳** — 检索最匹配的开源模板 |
| 🔨 **Drill Shell** — Clone and debug the environment until it runs | 🔨 **钻壳** — 克隆并调试环境直到能运行 |
| ✏️ **Modify Shell** — Understand the codebase and make targeted modifications | ✏️ **改壳** — 理解代码库并进行精准修改 |

---

## 🎯 Why PaGURUS? / 为什么选择 PaGURUS？

**[EN]** Unlike traditional LLM agents that generate code from zero-shot, PaGURUS ensures quality through template-based development and execution verification.

**[中文]** 与传统的零样本 LLM 智能体不同，PaGURUS 通过基于模板的开发和执行验证确保代码质量。

| **[EN] Traditional LLM Agents** | **[中文] 传统 LLM 智能体** | **PaGURUS** |
|:---|:---|:---|
| ❌ Zero-shot generation, unpredictable quality | ❌ 零样本生成，质量不可控 | ✅ Template-based, quality guaranteed / 基于模板，质量有保障 |
| ❌ No execution verification | ❌ 无执行验证 | ✅ Sandbox execution with validation / 沙盒执行验证 |
| ❌ Limited repository understanding | ❌ 仓库理解能力有限 | ✅ Global dependency graph (Repo Map) / 全局依赖图 |
| ❌ Manual environment setup | ❌ 手动配置环境 | ✅ Auto-debug until success / 自动调试至成功 |

---

## 🔄 Workflow / 工作流程

```
User Request / 用户需求
      ↓
🔍 Find / 找壳: Retrieve matching template from GitHub
      ↓
🔨 Drill / 钻壳: Clone + Auto-debug until it runs
      ↓
✏️ Modify / 改壳: Parse AST + Generate targeted patches
      ↓
✅ Verify / 验证: Re-compile + Self-heal on errors
      ↓
📦 Deliver / 交付: Complete, working project
```

---

## 🏗️ Architecture / 系统架构

**[EN]** PaGURUS consists of four core modules:

**[中文]** PaGURUS 由四个核心模块组成：

| **[EN] Module** | **[中文] 模块** | **Description / 描述** |
|:---|:---|:---|
| **Retriever** | **检索器** | Intent parsing and template matching / 意图解析与模板匹配 |
| **Sandbox** | **沙盒** | Isolated environment with auto-debug / 隔离环境与自动调试 |
| **Modifier** | **改造器** | AST-based code understanding and patching / 基于 AST 的代码理解与补丁 |
| **Validator** | **验证器** | Execution verification and self-healing / 执行验证与自修复 |

---

## 🛣️ Roadmap / 研发路线

| **[EN] Phase** | **[中文] 阶段** | **Timeline / 时间** | **Goals / 目标** |
|:---|:---|:---|:---|
| **PoC** | **概念验证** | 1 week / 1周 | Fixed template + manual debugging / 固定模板 + 手动调试 |
| **MVP** | **最小可行产品** | 1 month / 1月 | Auto-retrieval + sandbox + closed loop / 自动检索 + 沙盒 + 闭环 |
| **Research** | **研究深化** | 3 months / 3月 | Auto environment repair + repo-level understanding / 自动环境修复 + 仓库级理解 |

---

## 🚀 Quick Start / 快速开始

**[EN]**

```bash
# Example: Create a React blog with FastAPI backend

# ① Find: PaGURUS searches for "react-fastapi-starter"
# ② Drill: Auto-install dependencies and start services
# ③ Modify: Add blog components and authentication APIs
# ✅ Deliver: Production-ready project
```

**[中文]**

```bash
# 示例：创建一个带 FastAPI 后端的 React 博客

# ① 找壳：PaGURUS 搜索 "react-fastapi-starter"
# ② 钻壳：自动安装依赖并启动服务
# ③ 改壳：添加博客组件和认证 API
# ✅ 交付：生产就绪的项目
```

---

## 🔬 Key Innovations / 核心创新

| **[EN]** | **[中文]** |
|:---|:---|
| **Execution-Guided** — Real sandbox validation, not just static generation | **执行驱动** — 真实沙盒验证，而非静态生成 |
| **Repository-Level** — Global dependency understanding via Repo Map | **仓库级理解** — 通过 Repo Map 理解全局依赖 |
| **Template-First** — Leverage open-source ecosystem, not reinvent the wheel | **模板优先** — 利用开源生态，不重复造轮子 |
| **Self-Healing** — Dedicated debug agent for environment and code errors | **自修复** — 专门的调试代理处理环境和代码错误 |

---

## 📚 Tech Stack / 技术栈

| **[EN] Component** | **[中文] 组件** | **Technology / 技术选型** |
|:---|:---|:---|
| Sandbox | 沙盒环境 | Docker / E2B |
| Code Parsing | 代码解析 | Tree-sitter |
| Vector Search | 向量检索 | Qdrant |
| LLM | 大语言模型 | Claude 3.5 Sonnet / DeepSeek Coder |
| Diff Generation | 差异生成 | Aider-style patches |

---

## 🎓 Why "PaGURUS"? / 为什么叫 "PaGURUS"？

**[EN]**

> A hermit crab spends its life finding, drilling into, and modifying shells.
>
> **PaGURUS does the same with code**: find templates → make them work → improve them.
>
> Not starting from scratch, but building on the shoulders of open source.

**[中文]**

> 寄居蟹的一生都在寻找、钻入、改造合适的壳。
>
> **PaGURUS 也一样**：找模板 → 跑通环境 → 增量改造
>
> 不是从零开始，而是站在开源的肩膀上。

---

## 📖 Documentation / 文档

- [Concept Document (中文)](docs/CONCEPT.md) — Detailed concept explanation
- [Core Concept (中文)](docs/CONCEPT_CORE.md) — Quick overview
- [Architecture (中文)](docs/CONCEPT.md#系统架构-core-modules) — System architecture

---

## 🤝 Contributing / 贡献

**[EN]** This project is currently in the concept phase. Contributions and suggestions are welcome!

**[中文]** 本项目目前处于概念阶段。欢迎贡献和建议！

---

## 📄 License / 许可证

MIT License

---

**[EN]** Template is Quality, Execution is Truth 🦀

**[中文]** 模板即质量，执行即真理 🦀

---

*Status: Concept Phase / 概念阶段*  
*Last Updated: April 2026*

# 🦀 PaGURUS

> **Execution-Guided Repository-Level Code Agent**  
> *Clone, Build, and Tweak—Standing on the Shoulders of Open Source*

---

## 💡 What is PaGURUS?

**PaGURUS** is a repository-level code agent that generates code by **finding, running, and modifying** existing open-source templates, rather than generating from scratch.

### The Core Idea: **"Find Shell → Drill Shell → Modify Shell"**

Like a hermit crab that finds, occupies, and modifies shells, PaGURUS:
1. **🔍 Find Shell** — Search and retrieve the best-matching open-source template
2. **🔨 Drill Shell** — Clone and debug the environment until it runs
3. **✏️ Modify Shell** — Understand the codebase and make targeted modifications

---

## 🎯 Why PaGURUS?

| Traditional LLM Agents | PaGURUS |
|----------------------|---------|
| ❌ Zero-shot generation, unpredictable quality | ✅ Template-based, quality guaranteed |
| ❌ No execution verification | ✅ Sandbox execution with validation |
| ❌ Limited repository understanding | ✅ Global dependency graph (Repo Map) |
| ❌ Manual environment setup | ✅ Auto-debug until success |

---

## 🔄 Workflow

```
User Request
      ↓
🔍 Find: Retrieve matching template from GitHub
      ↓
🔨 Drill: Clone + Auto-debug until it runs
      ↓
✏️ Modify: Parse AST + Generate targeted patches
      ↓
✅ Verify: Re-compile + Self-heal on errors
      ↓
📦 Deliver: Complete, working project
```

---

## 🏗️ Architecture

PaGURUS consists of four core modules:

1. **Retriever** — Intent parsing and template matching
2. **Sandbox** — Isolated environment with auto-debug
3. **Modifier** — AST-based code understanding and patching
4. **Validator** — Execution verification and self-healing

---

## 🛣️ Roadmap

- [ ] **Phase 1 (PoC - 1 week)**: Fixed template + manual debugging
- [ ] **Phase 2 (MVP - 1 month)**: Auto-retrieval + sandbox + closed loop
- [ ] **Phase 3 (Research - 3 months)**: Auto environment repair + repository-level understanding

---

## 🚀 Quick Start

```bash
# Example: Create a React blog with FastAPI backend

# ① Find: PaGURUS searches for "react-fastapi-starter"
# ② Drill: Auto-install dependencies and start services
# ③ Modify: Add blog components and authentication APIs
# ✅ Deliver: Production-ready project
```

---

## 🔬 Key Innovations

- **Execution-Guided**: Real sandbox validation, not just static generation
- **Repository-Level**: Global dependency understanding via Repo Map
- **Template-First**: Leverage open-source ecosystem, not reinvent the wheel
- **Self-Healing**: Dedicated debug agent for environment and code errors

---

## 📚 Tech Stack

| Component | Technology |
|-----------|-----------|
| Sandbox | Docker / E2B |
| Code Parsing | Tree-sitter |
| Vector Search | Qdrant |
| LLM | Claude 3.5 Sonnet / DeepSeek Coder |
| Diff Generation | Aider-style patches |

---

## 🎓 Why "PaGURUS"?

> A hermit crab spends its life finding, drilling into, and modifying shells.
> 
> **PaGURUS does the same with code**: find templates → make them work → improve them.
> 
> Not starting from scratch, but building on the shoulders of open source.

---

**Template is Quality, Execution is Truth** 🦀

---

*Status: Concept Phase*  
*Last Updated: April 2026*

"""
AI Analyzer - 使用LLM分析架构文档并生成搜索策略
"""

import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from config import Config


class ArchitectureAnalyzer:
    """架构文档分析器"""

    def __init__(self):
        """初始化分析器"""
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError(
                "❌ API Key未设置!\n"
                "请在 .env 文件中设置 OPENAI_API_KEY\n"
                "\n支持的模型服务:\n"
                "- OpenAI: https://platform.openai.com/api-keys\n"
                "- 阿里云通义: https://dashscope.aliyuncs.com\n"
                "- 智谱AI: https://open.bigmodel.cn\n"
                "- DeepSeek: https://platform.deepseek.com"
            )

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        self.model = Config.OPENAI_MODEL

    def analyze_architecture(self, markdown_content: str) -> Dict[str, Any]:
        """
        分析架构文档，提取技术栈和模块

        Args:
            markdown_content: 架构文档的Markdown内容

        Returns:
            包含技术栈、模块、搜索策略的字典
        """
        prompt = f"""你是一个技术专家，擅长分析系统架构文档并推荐合适的开源项目。

请分析以下架构文档，提取出：
1. **技术栈**：前端框架、后端框架、数据库、中间件等
2. **功能模块**：系统的主要功能模块
3. **搜索策略**：为每个模块生成GitHub搜索关键词

请以JSON格式返回，格式如下：
{{
    "project_overview": "项目简要描述",
    "tech_stack": {{
        "frontend": ["框架1", "框架2"],
        "backend": ["框架1", "框架2"],
        "database": ["数据库1", "数据库2"],
        "middleware": ["中间件1"],
        "other": ["其他技术"]
    }},
    "modules": [
        {{
            "name": "模块名称",
            "description": "模块功能描述",
            "tech_requirements": ["需要的技术1", "需要的技术2"],
            "search_keywords": ["关键词1", "关键词2", "关键词3"],
            "github_search_queries": [
                "language:python 框架名",
                "language:javascript 模块名 starter"
            ]
        }}
    ],
    "additional_recommendations": [
        "建议1",
        "建议2"
    ]
}}

架构文档内容如下：
```
{markdown_content}
```

请只返回JSON，不要其他内容。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个技术专家，擅长分析架构和推荐开源项目。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.OPENAI_TEMPERATURE,
                max_tokens=Config.OPENAI_MAX_TOKENS
            )

            result = response.choices[0].message.content.strip()

            # 清理可能的markdown代码块标记
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            result = result.strip()

            # 解析JSON
            analysis = json.loads(result)
            return analysis

        except json.JSONDecodeError as e:
            raise ValueError(f"❌ AI返回的不是有效的JSON: {e}\n原始内容: {result}")
        except Exception as e:
            raise RuntimeError(f"❌ AI分析失败: {e}")

    def generate_search_queries(self, module: Dict[str, Any]) -> List[str]:
        """
        为模块生成额外的GitHub搜索查询

        Args:
            module: 模块信息字典

        Returns:
            搜索查询列表
        """
        queries = []

        # 基础查询
        base_keywords = module.get("search_keywords", [])
        tech_reqs = module.get("tech_requirements", [])

        # 组合生成查询
        for keyword in base_keywords:
            for tech in tech_reqs:
                # 尝试不同的语言映射
                lang_map = {
                    "python": "language:python",
                    "javascript": "language:javascript",
                    "typescript": "language:typescript",
                    "java": "language:java",
                    "go": "language:go",
                    "rust": "language:rust",
                    "c++": "language:cpp",
                    "react": "language:javascript react",
                    "vue": "language:javascript vue",
                    "angular": "language:javascript angular",
                    "next.js": "framework:next.js",
                    "express": "framework:express",
                    "django": "framework:django",
                    "flask": "framework:flask",
                    "fastapi": "framework:fastapi",
                    "spring": "framework:spring",
                }

                tech_lower = tech.lower()
                if tech_lower in lang_map:
                    queries.append(f"{lang_map[tech_lower]} {keyword}")
                else:
                    queries.append(f"{keyword} {tech}")

                # 添加starter/template相关的查询
                queries.append(f"{keyword} starter")
                queries.append(f"{keyword} template")
                queries.append(f"{keyword} boilerplate")

        return list(set(queries))  # 去重


def test_analyzer():
    """测试分析器"""
    # 测试用的架构文档
    test_architecture = """
    # 电商后台管理系统

    ## 技术栈
    - 前端：React + TypeScript + Ant Design
    - 后端：Node.js + Express + MongoDB
    - 缓存：Redis
    - 消息队列：RabbitMQ

    ## 系统模块

    ### 1. 用户管理模块
    - 用户注册、登录、权限管理
    - JWT认证
    - RBAC权限控制

    ### 2. 商品管理模块
    - 商品CRUD
    - 分类管理
    - 库存管理
    - 图片上传

    ### 3. 订单管理模块
    - 订单创建、支付、发货
    - 订单状态流转
    - 退款处理

    ### 4. 数据分析模块
    - 销售统计
    - 用户行为分析
    - 数据可视化
    """

    analyzer = ArchitectureAnalyzer()
    try:
        result = analyzer.analyze_architecture(test_architecture)
        print("✅ 分析成功!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    test_analyzer()

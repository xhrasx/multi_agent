"""
翻译工具
"""
import requests
from app.tools.tool_registry import registry


class TranslatorTool:
    name = "translator"
    description = "翻译文本，支持中英互译及多语言翻译"

    def run(self, text: str) -> str:
        try:
            api_key = "sk-poe-0b8uMtsIcvMsmHHvAwGSEQenw3O_Ae6AqHHBLFydDfQ"
            url = "https://api.poe.com/v1/chat/completions"

            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-5.3-codex",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是翻译专家。如果输入是中文就翻译成英文，"
                                       "如果输入是英文就翻译成中文。"
                                       "如果用户指定了目标语言就按要求翻译。"
                                       "只输出翻译结果，不要解释。"
                        },
                        {"role": "user", "content": text}
                    ]
                },
                timeout=30,
            )
            resp_json = response.json()
            result = resp_json["choices"][0]["message"]["content"]
            return f"🌐 翻译结果:\n{result}"
        except Exception as e:
            return f"翻译出错: {str(e)}"


# ✅ 注册到 registry（在类外面）
def translator_tool(text: str) -> str:
    return TranslatorTool().run(text)


registry.register(
    "translator",
    translator_tool,
    description=TranslatorTool.description,
)
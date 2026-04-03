import requests


class SearchTool:
    """搜索/知识查询工具（使用 LLM 模拟）"""

    name = "search"
    description = "搜索知识、百科、人物、事件、概念解释等"

    def __init__(self):
        self.api_key = ""
        self.url = ""
        self.model = ""

    def run(self, query: str) -> str:
        try:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个知识搜索引擎。请用简洁准确的中文回答问题，"
                                       "控制在200字以内。如果不确定请说明。"
                        },
                        {"role": "user", "content": query}
                    ]
                }
            )
            resp_json = response.json()
            return resp_json["choices"][0]["message"]["content"]
        except Exception as e:
            return f"搜索出错: {str(e)}"
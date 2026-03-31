"""
LLM 推理器 - 自动任务分类
"""
import json
import time
import requests


class LLMReasoner:

    def __init__(self):
        self.api_key = "sk-poe-0b8uMtsIcvMsmHHvAwGSEQenw3O_Ae6AqHHBLFydDfQ"
        self.url = "https://api.poe.com/v1/chat/completions"
        self.model = "gpt-5.3-codex"

    def reason(self, user_input, memory):
        history = memory.get_context()

        prompt = f"""你是一个智能任务调度Agent。分析用户问题，选择最合适的工具。

## 可用工具：

| 工具名 | 用途 | input示例 |
|--------|------|-----------|
| calculator | 数学计算、算术 | "2+4", "sqrt(16)" |
| search | 知识查询、百科、概念、编程 | "什么是量子计算" |
| weather | 天气查询 | "北京", "上海" |
| datetime | 日期时间查询 | "现在几点" |
| translator | 翻译文本 | "Hello World" |

## 分类规则：
- 数字运算、加减乘除、数学公式 → calculator
- 天气、温度、下雨、气温 → weather（input只填城市名）
- 时间、日期、星期、几号 → datetime
- 翻译、translate、英译中、中译英 → translator
- 知识问题、是什么、为什么、怎么做 → search
- 简单问候、闲聊 → finish

## 严格输出JSON（不要任何多余文字）：
{{
    "type": "tool" 或 "finish",
    "tool": "工具名（finish时留空字符串）",
    "input": "传给工具的参数 或 直接回答"
}}

## 示例：
用户: "3+5等于多少" → {{"type":"tool","tool":"calculator","input":"3+5"}}
用户: "北京天气" → {{"type":"tool","tool":"weather","input":"北京"}}
用户: "现在几点" → {{"type":"tool","tool":"datetime","input":"现在几点"}}
用户: "什么是AI" → {{"type":"tool","tool":"search","input":"什么是AI"}}
用户: "翻译你好" → {{"type":"tool","tool":"translator","input":"你好"}}
用户: "你好" → {{"type":"finish","tool":"","input":"你好！有什么可以帮你的？"}}

---
历史记录：{history}
用户问题：{user_input}
"""

        start_time = time.time()

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        elapsed = round(time.time() - start_time, 3)
        print("Status Code:", response.status_code)
        print("Response:", response.text[:300])

        resp_json = response.json()
        print("🔍 LLM 原始响应:", resp_json)
        content = resp_json["choices"][0]["message"]["content"]
        usage = resp_json.get("usage", {})

        meta = {
            "model": resp_json.get("model", self.model),
            "latency_seconds": elapsed,
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "finish_reason": resp_json["choices"][0].get("finish_reason"),
            "status_code": response.status_code,
        }

        # 清理 markdown 包裹
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {
                "type": "finish",
                "tool": "",
                "input": content
            }

        return parsed, meta
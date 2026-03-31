"""任务拆解
后续你可以升级成 LLM 拆解版本
"""
class PlannerAgent:

    def plan(self, user_input: str):
        if "计算" in user_input:
            return [{"tool": "calculator", "input": user_input.replace("计算", "")}]
        elif "搜索" in user_input:
            return [{"tool": "search", "input": user_input}]
        else:
            return [{"tool": "search", "input": user_input}]
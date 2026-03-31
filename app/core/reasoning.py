class ReasoningAgent:

    def reason(self, goal, memory):

        if "计算" in goal:
            expression = goal.replace("计算", "")
            return {
                "type": "tool",
                "tool": "calculator",
                "input": expression
            }

        return {
            "type": "finish",
            "output": "无法处理"
        }
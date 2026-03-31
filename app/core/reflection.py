class ReflectionAgent:

    def reflect(self, memory):

        history = memory.get_context()

        # 简单示例：如果结果为空，重新尝试
        if not history:
            return

        last = history[-1]

        if "observation" in last:
            if last["observation"] == "":
                memory.add("reflection", "上一步失败，需要重新尝试")
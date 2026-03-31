class Router:

    def route(self, task: dict):
        tool_name = task.get("tool")
        tool_input = task.get("input")

        # 1️⃣ 成本控制示例
        if tool_name == "llm":
            if len(tool_input) < 20:
                task["model"] = "small-model"
            else:
                task["model"] = "large-model"

        # 2️⃣ 失败回退策略
        task["retry"] = 2

        # 3️⃣ 优先级调度
        task["priority"] = "high" if "紧急" in tool_input else "normal"

        return task
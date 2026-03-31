class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool):
        self.tools[name] = tool

    def get(self, name: str):
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name]
# ✅ 全局单例
registry = ToolRegistry()
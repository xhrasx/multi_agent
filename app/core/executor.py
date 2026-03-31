"""
执行器 - 通过 registry 路由工具
"""
from app.tools.tool_registry import registry  # ← 导入全局单例，不是类


class ExecutorAgent:

    def __init__(self):
        self.registry = registry  # ← 用全局单例，不是 new 一个新的

    def execute(self, action: dict) -> str:
        tool_name = action.get("tool", "")
        tool_input = action.get("input", "")

        print(f"  🔧 调用工具: {tool_name}({tool_input})")
        return self.registry.execute(tool_name, tool_input)

    def list_tools(self) -> dict:
        return self.registry.list_tools_detail()
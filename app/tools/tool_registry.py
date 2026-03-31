"""
工具注册中心
"""


class ToolRegistry:

    def __init__(self):
        self.tools = {}
        self.descriptions = {}

    def register(self, name: str, func, description: str = ""):
        """注册工具：名称、函数、描述"""
        self.tools[name] = func
        self.descriptions[name] = description

    def get(self, name: str):
        """获取工具函数"""
        return self.tools.get(name)

    def execute(self, name: str, input_text: str) -> str:
        """执行指定工具"""
        func = self.tools.get(name)
        if func is None:
            available = ", ".join(self.tools.keys())
            return f"❌ 未知工具: {name}。可用工具: {available}"
        try:
            return func(input_text)
        except Exception as e:
            return f"❌ 工具 {name} 执行出错: {str(e)}"

    def list_tools(self) -> list:
        """列出所有工具名"""
        return list(self.tools.keys())

    def list_tools_detail(self) -> dict:
        """列出所有工具及描述"""
        return {
            name: self.descriptions.get(name, "无描述")
            for name in self.tools
        }


registry = ToolRegistry()
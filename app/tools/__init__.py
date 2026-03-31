"""
工具包初始化
"""
from app.tools.tool_registry import registry

from app.tools.calculator import CalculatorTool
from app.tools.search import SearchTool
from app.tools.weather import WeatherTool
from app.tools.datetime_tool import DateTimeTool
from app.tools.translator import TranslatorTool

# 类实例注册表
TOOL_REGISTRY = {
    "calculator": CalculatorTool(),
    "search": SearchTool(),
    "weather": WeatherTool(),
    "datetime": DateTimeTool(),
    "translator": TranslatorTool(),
}

# ✅ 关键：同步到 registry 单例
for name, tool_instance in TOOL_REGISTRY.items():
    desc = getattr(tool_instance, "description", "无描述")
    registry.register(name, tool_instance.run, description=desc)

print(f"✅ 已注册工具: {registry.list_tools()}")


def get_tools_detail() -> list:
    result = []
    for name, tool_instance in TOOL_REGISTRY.items():
        result.append({
            "name": name,
            "description": getattr(tool_instance, "description", "无描述"),
            "status": "active",
        })
    return result
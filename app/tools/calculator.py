"""
计算器工具
"""
import math
from app.tools.tool_registry import registry


class CalculatorTool:
    name = "calculator"
    description = "数学计算，如 2+4、sqrt(16)、3**2+5"

    def run(self, input_text: str) -> str:
        try:
            allowed = {
                "__builtins__": {},
                "abs": abs, "round": round,
                "min": min, "max": max,
                "sum": sum, "pow": pow,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e,
                "log": math.log,
                "log10": math.log10,
            }
            result = eval(input_text, allowed)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"


# 兼容 registry 单例
def calculator_tool(input_text: str):
    return CalculatorTool().run(input_text)


registry.register("calculator", calculator_tool, description=CalculatorTool.description)
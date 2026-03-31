from datetime import datetime


class DateTimeTool:
    """日期时间工具"""

    name = "datetime"
    description = "查询当前日期、时间、星期几、倒计时计算等"

    def run(self, query: str) -> str:
        try:
            now = datetime.now()
            return (
                f"📅 当前时间信息:\n"
                f"  日期: {now.strftime('%Y年%m月%d日')}\n"
                f"  时间: {now.strftime('%H:%M:%S')}\n"
                f"  星期: 星期{['一','二','三','四','五','六','日'][now.weekday()]}\n"
                f"  时间戳: {int(now.timestamp())}"
            )
        except Exception as e:
            return f"时间查询出错: {str(e)}"
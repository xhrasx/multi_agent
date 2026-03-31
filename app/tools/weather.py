import requests


class WeatherTool:
    """天气查询工具（使用免费API）"""

    name = "weatherTool"
    description = "查询城市天气，如：北京天气、上海天气"

    def run(self, city: str) -> str:
        try:
            # 使用免费天气 API（wttr.in）
            city_clean = city.replace("天气", "").replace("的", "").strip()
            url = f"https://wttr.in/{city_clean}?format=j1&lang=zh"
            resp = requests.get(url, timeout=10)
            data = resp.json()

            current = data["current_condition"][0]
            temp = current["temp_C"]
            humidity = current["humidity"]
            desc = current.get("lang_zh", [{}])
            if desc:
                weather_desc = desc[0].get("value", current["weatherDesc"][0]["value"])
            else:
                weather_desc = current["weatherDesc"][0]["value"]

            return (
                f"🌤 {city_clean} 当前天气:\n"
                f"  温度: {temp}°C\n"
                f"  湿度: {humidity}%\n"
                f"  天气: {weather_desc}"
            )
        except Exception as e:
            return f"天气查询出错: {str(e)}，请检查城市名是否正确"
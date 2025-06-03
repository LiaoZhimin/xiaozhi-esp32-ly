
from plugins_func.register import register_function, ToolType, ActionResponse, Action

GET_WEATHER_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "获取某个地点的天气，用户应提供一个位置，比如用户说杭州天气，参数为：杭州。"
            "如果用户说的是省份，默认用省会城市。如果用户说的不是省份或城市而是一个地名，默认用该地所在省份的省会城市。"
            "如果用户没有指明地点，说“天气怎么样”，”今天天气如何“，location参数为空"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "地点名，例如杭州。可选参数，如果不提供则不传",
                }
            },
            "required": ["lang"],
        },
    },
}

@register_function("get_weather_test", GET_WEATHER_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def get_weather_test(conn, location: str = None):
    return ActionResponse(Action.REQLLM, f"{location}当前天气：阴，温度：23°C，湿度：50%，风速：10km/h", None) 
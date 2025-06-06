import http.client
import json

from plugins_func.register import register_function, ToolType, ActionResponse, Action

DESC = {
    "type": "function",
    "function": {
        "name": "my_handle_device",
        "description": (
            "调用IOT Server的API，进行控制设备，用户传空间ID和场景ID"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "spc_id": {
                    "type": "string",
                    "description": "空间ID，例如：客厅:1",
                },
                "scn_id": {
                    "type": "string",
                    "description": "场景ID，例如：日常:3",
                }
            },
            "required": ["spc_id", "scn_id"],
        },
    },
}

@register_function("my_handle_device", DESC, ToolType.IOT_CTL)
def my_handle_device(conn, spc_id, scn_id, content:str = ""):
    try:
        base_url = conn.config["plugins"]["my_handle_device"]["base_url"] # "localhost:8080"
        api_path = conn.config["plugins"]["my_handle_device"]["api_path"] # "/v1/iot/Scene"
        conn = http.client.HTTPSConnection(base_url)
        payload = json.dumps({
           "Mac": "e816568686b6",
           "SceneId": scn_id,
           "RoomId": spc_id
        })
        headers = {
           "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
           "Content-Type": "application/json",
           "Accept": "*/*",
           "Host": base_url,
           "Connection": "keep-alive"
        }
        conn.request("POST", api_path, payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            return ActionResponse(Action.RESPONSE, content, content)
    except Exception as e:
        print(f"Error in response generation: {e}")
    return ActionResponse(Action.RESPONSE, "操作失败", "操作失败")
    ## 注意，一定要返回ActionResponse固定的对象，Action.RESPONSE表示直接进行后续的语音合成；
    ## Action.LLM 表示还会跳转到调用LLM的步骤，将结果进行LLM的二次处理和操作
    ## （注意如果LLM操作结果是函数调用，则会无限循环，所以最好function_call的都要使用Action.RESPONSE）。
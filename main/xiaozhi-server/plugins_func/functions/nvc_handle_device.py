import http.client
import json

from plugins_func.register import register_function, ToolType, ActionResponse, Action

DESC = {
    "type": "function",
    "function": {
        "name": "nvc_handle_device",
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

@register_function("nvc_handle_device", DESC, ToolType.IOT_CTL)
def nvc_handle_device(conn, spc_id, scn_id, content:str = None):
    try:
        base_url = conn.config["plugins"]["nvc_handle_device"]["base_url"] # "testapi.nvc-smart.com"
        conn = http.client.HTTPSConnection(base_url)
        payload = json.dumps({
           "Mac": "e816568686b6",
           "SceneId": scn_id,
           "RoomId": spc_id
        })
        headers = {
           'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
           'Content-Type': 'application/json',
           'Accept': '*/*',
           'Host': base_url,
           'Connection': 'keep-alive'
        }
        conn.request("POST", "/v1/udpserver/ExternalCtrl/Scene", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            return ActionResponse(Action.REQLLM, content, None)
    except Exception as e:
        print(f"Error in response generation: {e}")
    return ActionResponse(Action.REQLLM, "操作失败", None)
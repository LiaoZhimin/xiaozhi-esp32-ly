
import requests
import json


def start_qwen3_vllm_api_client(url, model, prompt_text, user_text):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": prompt_text
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        "temperature": 0.7,
        "top_p": 0.8,
        "repetition_penalty": 1.05,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # print('请求成功，响应内容：')
        print("responce json: ", response.json(), '\n')
        # print("responce content: ", response.content, '\n')
        # print("responce text: ", response.text, '\n')
        return response.json()
    else:
        print(f'请求失败，状态码: {response.status_code}，错误信息: {response.text}')
        
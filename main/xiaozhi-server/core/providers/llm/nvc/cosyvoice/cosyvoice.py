
from typing import Any
import requests



async def  cosyvoice_api_client(url, prompt_wav_file_path, prompt_text, tts_text)-> bytes|Any:
    files = {
        'prompt_wav': open(prompt_wav_file_path, 'rb')
    }

    payload = {
        'tts_text': tts_text,
        'prompt_text': prompt_text
    }

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        with open('output_audio_0002.pcm', 'wb') as f:
            f.write(response.content)
        print('文件已成功保存为 output_audio_0002.pcm')
        return response.content
    else:
        print(f'请求失败，状态码: {response.status_code}，错误信息: {response.text}')
        return None
        
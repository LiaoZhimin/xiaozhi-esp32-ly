import os
import uuid
import requests
from config.logger import setup_logging
from datetime import datetime
from core.providers.tts.base import TTSProviderBase
from core.providers.nvc.cosyvoice.cosyvoise import cosyvoice_api_client

TAG = __name__
logger = setup_logging()

class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)
        self.url = config.get("url")
        self.prompt_wav_file_path = config.get("prompt_wav_file_path")
        self.prompt_text = config.get("prompt_text")
        self.output_file = config.get("output_dir", "tmp/")
        self.format = config.get("format", "wav")

    def generate_filename(self):
        fn = os.path.join(self.output_file, f"tts-{datetime.now().date()}@{uuid.uuid4().hex}.{self.format}")
        logger.bind(tag=TAG).info(f"生成的文件名: {fn}")
        return fn
    
    
    async def text_to_speak(self, text, output_file):  
        logger.bind(tag=TAG).info(f"cosyvoice调用开始: URL:  {self.url}  PromptWavFilePath : {self.prompt_wav_file_path} PromptText:{self.prompt_text} UserInput: {text} ")
        opus_datas = await cosyvoice_api_client(self.url, self.prompt_wav_file_path, self.prompt_text, text)
        with open(output_file, "wb") as file:
            file.write(opus_datas)


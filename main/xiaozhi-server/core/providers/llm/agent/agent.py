import json

from config.logger import setup_logging
from core.providers.llm.base import LLMProviderBase
from core.providers.nvc.agent.agent import new_session, ask_agent, delete_session


TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.url = config.get("base_url")
        self.api_key= config.get("api_key")
        self.agent_id= config.get("agent_id")
        self.is_think = config.get("is_think", False)

    def new_session(self):
        session_id = new_session(self.url, self.api_key, self.agent_id)
        return session_id
    
    def delete_session(self, session_id):
        delete_session(self.url, self.api_key, self.agent_id, session_id)
        
    
    def get_completion(self, session_id, prompts)->str:
        if session_id is None:
            return "请先创建对话"
        outputs = ask_agent(self.url, self.api_key,self.agent_id, prompts, session_id)
        return outputs


    def response(self, session_id, dialogue):
        try:
            last_msg = next(m for m in reversed(dialogue) if m["role"] == "user")
            user_input = last_msg.get("content", last_msg)
            if not self.is_think:
                user_input += "//no_thinking"
            logger.bind(tag=TAG).info(f"[{session_id}] 》》》agent调用开始: URL:  {self.url}  session_id : {session_id} UserInput: {user_input} ")
            ret = self.get_completion(session_id, last_msg)
            logger.bind(tag=TAG).info(f"[{session_id}] 》》》agent调用结束: URL:  outputs: {ret} ")
            yield ret
        except Exception as e:
            logger.bind(tag=TAG).error(f"[{session_id}] Error in response generation: {e}")


    def response_with_functions(self, session_id, dialogue, functions=None):
        try:
            last_msg = next(m for m in reversed(dialogue) if m["role"] == "user")
            user_input = last_msg.get("content", last_msg)
            logger.bind(tag=TAG).info(f"[{session_id}] 》》》agent func begin,  URL:  {self.url}  session_id : {session_id} UserInput: {user_input} ")
            messages = self.get_completion(session_id, user_input)
            logger.bind(tag=TAG).info(f"[{session_id}] 》》》agent fun end , URL:  outputs: {messages}  类型: {type(messages)}")
            # 判断messages是否是json
            if isinstance(messages, str) and messages.find("{")>-1 and messages.find("}")>-1:
                messages = messages.replace("```json", "").replace("```", "").replace("\\","").replace("\xa0", "")
                obj = json.loads(messages)  # 解析为JSON对象
                yield "", [obj]
            else:
                yield messages, []
        except Exception as e:
            logger.bind(tag=TAG).error(f"[{session_id}] 》》》agent fun end , Error: {e}")
            yield  f"未获取到相应信息", None


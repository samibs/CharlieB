print("llm_studio_llm.py is being executed") # added print statement
import requests
import logging
from llama_index.core.llms import LLM, ChatMessage, ChatResponse

logging.basicConfig(level=logging.INFO)

class LLMMetadata:
    def __init__(self, model_name, context_window=4096, num_output=256, system_role="system", is_chat_model=True):
        self.model_name = model_name
        self.context_window = context_window
        self.num_output = num_output
        self.system_role = system_role
        self.is_chat_model = is_chat_model

class LMStudioLLM(LLM):
    endpoint: str = "http://127.0.0.1:1234/v1/chat/completions"
    model: str = "meta-llama-3-8b-instruct"

    def complete(self, prompt: str, **kwargs):
        try:
            response = requests.post(
                self.endpoint,
                headers={"Content-Type": "application/json", "Authorization": "Bearer lm-studio"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}]},
            )
            response.raise_for_status()
            result = response.json()
            message_content = result["choices"][0]["message"]["content"]
            chat_message = ChatMessage(role="assistant", content=message_content)
            chat_response = ChatResponse(message=chat_message)
    
            logging.info(f"ChatResponse type: {type(chat_response)}")
            logging.info(f"ChatResponse message: {chat_response.message}")
            logging.info(f"ChatResponse message content: {chat_response.message.content}")
    
            return chat_response
        except requests.exceptions.RequestException as e:
            logging.error(f"LM Studio LLM request failed: {e}, Response: {e.response.text if e.response else 'No response'}", exc_info=True)
            return f"Error: {e}"

    async def acomplete(self, prompt: str, **kwargs):
        return self.complete(prompt, **kwargs)

    def chat(self, messages, **kwargs):
        system_message = next((msg for msg in messages if msg.role == "system"), None)
        user_messages = [msg.content for msg in messages if msg.role == "user"]
        if system_message:
            prompt = f"{system_message.content}\n" + "\n".join(user_messages)
        else:
            prompt = "\n".join(user_messages)
        return self.complete(prompt, **kwargs)

    async def achat(self, messages, **kwargs):
        return self.chat(messages, **kwargs)

    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Streaming not supported")

    async def astream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Streaming not supported")

    def stream_chat(self, messages, **kwargs):
        raise NotImplementedError("Streaming not supported")

    async def astream_chat(self, messages, **kwargs):
        raise NotImplementedError("Streaming not supported")

    @property
    def metadata(self):
        return LLMMetadata(model_name=self.model)
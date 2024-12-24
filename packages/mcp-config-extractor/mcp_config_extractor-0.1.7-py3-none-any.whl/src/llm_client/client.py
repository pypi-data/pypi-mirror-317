from typing import List, Dict, Optional
from openai import OpenAI
import asyncio
from concurrent.futures import ThreadPoolExecutor

class LLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        http_referer: str = "https://github.com/scraper",
        title: str = "LLM Client"
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": http_referer,
                "X-Title": title,
            }
        )
        self.executor = ThreadPoolExecutor()
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt: Optional[str] = None

    def reset_conversation(self):
        self.conversation_history = []
        self.system_prompt = None

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    async def generate_completion(
        self, 
        prompt: str, 
        model: str = "gpt-3.5-turbo",
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        remember: bool = True
    ) -> str:
        try:
            messages = []
            
            # Add system message if provided
            system = system_prompt or self.system_prompt
            if system:
                messages.append({"role": "system", "content": system})
            
            # Add conversation history
            history = conversation_history if conversation_history is not None else self.conversation_history
            messages.extend(history)
            
            # Add the current user prompt
            messages.append({"role": "user", "content": prompt})
            
            # Run the API call in a thread pool
            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                self.executor,
                lambda: self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history if remember is True
            if remember:
                self.conversation_history.extend([
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}
                ])
            
            return response
        except Exception as e:
            print(f"Error generating completion: {e}")
            return ""

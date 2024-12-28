from .base import Feature

from fastapi import  WebSocket
from visionlite import visionai

class WebSearchAgent(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None,**kwargs):
        local_base_url=self.model_service.config.base_url.replace("/v1", "")
        google_res = visionai(message,
                              model=self.model_service.config.model_name,
                              base_url=local_base_url)
        udpated_message = (f"### Google Result {google_res}\n"
                           f"Now based on Google search , answer user query by saying "
                           f"Using google results / Without Google results\n"
                           f"now user query: {message}")
        await self.model_service.stream_response(websocket, udpated_message, system_prompt)



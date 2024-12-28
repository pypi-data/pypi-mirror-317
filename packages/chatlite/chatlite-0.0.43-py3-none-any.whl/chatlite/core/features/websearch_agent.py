from .base import Feature

from fastapi import  WebSocket
from visionlite import visionai

class WebSearchAgent(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None):
        google_res = visionai(message)
        udpated_message = (f"### Google Result {google_res}\n"
                           f"Now based on Google search results answer user query by saying "
                           f"Using google results / Without Google results\n"
                           f"now user query: {message}")
        await self.model_service.stream_response(websocket, udpated_message, system_prompt)



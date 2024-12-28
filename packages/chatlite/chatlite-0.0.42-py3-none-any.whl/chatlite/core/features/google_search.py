from .handle_google_search import handle_google_search
from fastapi import WebSocket
from .base import Feature
class GoogleSearchFeature(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str):
        await handle_google_search(
            websocket,
            message,
            self.model_service.config.model_name,
            system_prompt
        )

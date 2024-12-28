from abc import ABC, abstractmethod

from fastapi import WebSocket

class Feature(ABC):
    """Base class for all chat features"""

    def __init__(self, model_service):
        self.model_service = model_service

    @abstractmethod
    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None):
        """Handle the feature-specific logic"""
        pass


class DefaultChatFeature(Feature):
    """Default chat feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None):
        await self.model_service.stream_response(websocket, message, system_prompt,chat_history=chat_history)
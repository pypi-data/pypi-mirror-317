
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uvicorn
from .config import ModelConfig
from .features import (
    DefaultChatFeature,WebSearchAgent,EmailAssistantFeature,Feature,FastGoogleSearch,
RawWebSearchAgent
)
from .model_service import ModelService

class ChatServer:
    """Unified server implementation with feature support"""

    def __init__(self, model_config: ModelConfig):
        self.app = FastAPI()
        self.model_service = ModelService(model_config)
        self.features = self._initialize_features()
        self.setup_routes()

    def _initialize_features(self) -> Dict[str, Feature]:
        """Initialize available features"""
        return {
            'WebSearchAgent': WebSearchAgent(self.model_service),
            'email': EmailAssistantFeature(self.model_service),
            'chat': DefaultChatFeature(self.model_service),
            'is_websearch_chat':FastGoogleSearch(self.model_service),
            'RawWebSearchAgent':RawWebSearchAgent(self.model_service),
        }

    def setup_routes(self):
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            print(f"Client {client_id} connected")

            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    print(f"Received message from client: {message_data}")

                    user_message = message_data["message"]
                    system_prompt = message_data.get("system_prompt", "You are a helpful AI assistant.")
                    app_type = message_data.get("app_type", "chat")
                    agent_type = message_data.get("agent_type", None)
                    is_websearch_chat=message_data.get("is_websearch_chat", False)
                    chat_history=message_data.get("chat_history",[])

                    # Get the appropriate feature handler
                    if is_websearch_chat and agent_type not in ['WebSearchAgent','RawWebSearchAgent']:
                        feature = self.features["is_websearch_chat"]
                    elif agent_type:
                        feature = self.features.get(agent_type, self.features['chat'])
                    else:
                        feature = self.features.get(app_type, self.features['chat'])

                    await feature.handle(websocket, user_message, system_prompt,
                                         chat_history=chat_history)

            except WebSocketDisconnect:
                print(f"Client {client_id} disconnected")
            except Exception as e:
                print(f"Error in websocket endpoint: {str(e)}")

    def run(self, host: str = "0.0.0.0", port: int = 8143):
        """Start the server"""
        uvicorn.run(self.app, host=host, port=port, log_level="debug")

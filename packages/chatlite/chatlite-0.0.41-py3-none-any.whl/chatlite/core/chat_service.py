
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uvicorn
from .config import ModelConfig
from .features import DefaultChatFeature,GoogleSearchFeature,EmailAssistantFeature,Feature
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
            'google': GoogleSearchFeature(self.model_service),
            'email': EmailAssistantFeature(self.model_service),
            'chat': DefaultChatFeature(self.model_service)
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

                    # Get the appropriate feature handler
                    feature = self.features.get(app_type, self.features['chat'])
                    await feature.handle(websocket, user_message, system_prompt)

            except WebSocketDisconnect:
                print(f"Client {client_id} disconnected")
            except Exception as e:
                print(f"Error in websocket endpoint: {str(e)}")

    def run(self, host: str = "0.0.0.0", port: int = 8143):
        """Start the server"""
        uvicorn.run(self.app, host=host, port=port, log_level="debug")

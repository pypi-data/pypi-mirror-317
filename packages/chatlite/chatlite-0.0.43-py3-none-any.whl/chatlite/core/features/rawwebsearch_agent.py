from .base import Feature


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from visionlite._vision_ai import visionai

def streamer(res):
    for x in res.split(" "):
        yield x+" "


async def handle_google_search(websocket: WebSocket, message: str,model:str, system_prompt: str):
    """Handle Google search-like responses"""
    try:
        res = visionai(message)
        for chunk in streamer(res):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk,
                "type": "stream"
            }))
            await asyncio.sleep(0.01)

        await websocket.send_text(json.dumps({
            "sender": "bot",
            "type": "end_stream"
        }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "message": f"Error: {str(e)}",
            "type": "error"
        }))

class RawWebSearchAgent(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None):
        await handle_google_search(
            websocket,
            message,
            self.model_service.config.model_name,
            system_prompt
        )



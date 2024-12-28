from fastapi import WebSocket
from .base import Feature

import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from visionlite import avision,vision

def streamer(res):
    for x in res.split(" "):
        yield x+" "


async def handle_google_search(websocket: WebSocket, message: str,model:str, system_prompt: str):
    """Handle Google search-like responses"""
    try:
        res = await avision(message,k=3,max_urls=3)
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

class FastGoogleSearch(Feature):
    """Google search feature implementation"""

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None,**kwargs):
        google_res = await avision(message)
        udpated_message = (f"### Google Result {google_res}\n"
                           f"using purely google results provide answer for user query: \n"
                           f"if results are youtube urls then return them as it is"
                           f"{message}")

        await self.model_service.stream_response(websocket, udpated_message, system_prompt)



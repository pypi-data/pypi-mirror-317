import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio
from visionlite import avision

def streamer(res):
    for x in res.split(" "):
        yield x+" "


async def handle_google_search(websocket: WebSocket, message: str,model:str, system_prompt: str):
    """Handle Google search-like responses"""
    try:
        system_prompt = "You are a Google search assistant. Provide search-like results and snippets."
        res = await avision(message)
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
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI
import asyncio

app = FastAPI()

# Initialize OpenAI client for Ollama
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)


async def stream_ollama_response(websocket: WebSocket, message: str, model: str, system_prompt: str):
    """Stream response from Ollama using OpenAI client"""
    try:
        # Print for debugging
        print(f"Starting stream with model: {model}")
        print(f"System prompt: {system_prompt}")
        print(f"User message: {message}")

        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            stream=True  # Enable streaming
        )

        for chunk in stream:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                # Print for debugging
                print(f"Streaming token: {chunk.choices[0].delta.content}")

                # Send each token as it arrives
                await websocket.send_text(json.dumps({
                    "sender": "bot",
                    "message": chunk.choices[0].delta.content,
                    "type": "stream"
                }))

                # Add a small delay to make streaming visible
                await asyncio.sleep(0.01)

        # Send end of stream marker
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "type": "end_stream"
        }))
        print("Stream completed")

    except Exception as e:
        print(f"Error in streaming: {str(e)}")
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "message": f"Error: {str(e)}",
            "type": "error"
        }))


async def handle_google_search(websocket: WebSocket, message: str,model:str, system_prompt: str):
    """Handle Google search-like responses"""
    try:
        system_prompt = "You are a Google search assistant. Provide search-like results and snippets."
        stream = client.chat.completions.create(
            model=model,  # or your preferred model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            stream=True
        )

        for chunk in stream:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                await websocket.send_text(json.dumps({
                    "sender": "bot",
                    "message": chunk.choices[0].delta.content,
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


async def handle_email_assistant(websocket: WebSocket, message: str,model:str, system_prompt: str):
    """Handle email assistant responses"""
    try:
        system_prompt = "You are an email assistant. Help compose and format professional emails."
        stream = client.chat.completions.create(
            model=model,  # or your preferred model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            stream=True
        )

        for chunk in stream:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                await websocket.send_text(json.dumps({
                    "sender": "bot",
                    "message": chunk.choices[0].delta.content,
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


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    print(f"Client {client_id} connected")

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            print(f"Received message from client: {message_data}")

            user_message = message_data["message"]
            model = message_data["model"]
            system_prompt = message_data.get("system_prompt", "You are a helpful AI assistant.")
            app_type = message_data.get("app_type", "chat")  # New field for app type

            # Route to appropriate handler based on app_type
            if app_type == "google":
                await handle_google_search(websocket, user_message, model, system_prompt)
            elif app_type == "email":
                await handle_email_assistant(websocket,
                                             message=user_message,
                                             model=model,
                                             system_prompt=system_prompt)
            else:
                await stream_ollama_response(websocket, message=user_message,
                                             model=model,
                                             system_prompt=system_prompt)

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    except Exception as e:
        print(f"Error in websocket endpoint: {str(e)}")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
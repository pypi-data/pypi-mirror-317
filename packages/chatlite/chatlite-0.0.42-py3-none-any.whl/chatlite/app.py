from typing import Optional
from chatlite.core._types._hf_type import HFModelType
from chatlite.core.config import ModelConfig
from chatlite.core import ChatServer

def create_server(
    model_type: str="local",
    model_name: Optional[HFModelType]|str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4000,
    **kwargs
) -> ChatServer:
    """Create a unified server instance"""
    config = ModelConfig.create(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    return ChatServer(config)

def server(
    model_type: str="local",
    model_name: Optional[HFModelType]|str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4000,
    **kwargs
):
    """Create a default server instance"""
    _app = create_server(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    _app.run()

if __name__ == '__main__':
    server()

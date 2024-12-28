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
    base_url: Optional[str] = None,
    **kwargs
) -> ChatServer:
    """Create a unified server instance"""
    config = ModelConfig.create(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        **kwargs
    )
    return ChatServer(config)

def server(
    model_type: str="local",
    model_name: Optional[HFModelType]|str = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4000,
    base_url: Optional[str] = None,
    **kwargs
):
    """Create a default server instance"""
    _app = create_server(
        model_type=model_type,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        base_url=base_url,
        **kwargs
    )
    _app.run()


class HF:
    def __call__(self,
        model_name="NousResearch/Hermes-3-Llama-3.1-8B",
                 model_type='huggingface',*args, **kwargs):
        return server(
            model_type=model_type,
            model_name=model_name,
            *args,
            **kwargs
        )
    def models(self):
        for x in [
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "01-ai/Yi-1.5-34B-Chat",
    "codellama/CodeLlama-34b-Instruct-hf",
    "google/gemma-1.1-7b-it",
    "google/gemma-2-2b-it",
    "google/gemma-2-9b-it",
    "google/gemma-2b-it",
    "HuggingFaceH4/starchat2-15b-v0.1",
    "HuggingFaceH4/zephyr-7b-alpha",
    "HuggingFaceH4/zephyr-7b-beta",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "microsoft/DialoGPT-medium",
    "microsoft/Phi-3-mini-4k-instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "Qwen/Qwen2.5-3B-Instruct",
    "tiiuae/falcon-7b-instruct",
    "uschreiber/llama3.2"
]:
            print(x)


huggingface = HF()

if __name__ == '__main__':
    server(
        model_type='huggingface',
        model_name="NousResearch/Hermes-3-Llama-3.1-8B"
    # base_url="http://192.168.170.76:11434/v1",
    #     model_name="qwen2.5:7b-instruct"
    )

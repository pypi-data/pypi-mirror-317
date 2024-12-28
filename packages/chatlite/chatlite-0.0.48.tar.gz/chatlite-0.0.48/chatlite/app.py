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




def local_qwen2p5(
    base_url="http://0.0.0.0:11434/v1",
    model_name="qwen2.5:0.5b-instruct",
    *args,
    **kwargs
):
    return server(
        model_type="huggingface",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )


def local_llama3p2(
    base_url="http://0.0.0.0:11434/v1",
    model_name="llama3.2:latest",
    *args,
    **kwargs
):
    return server(
        model_type="huggingface",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )


def local_qwen7b(
    base_url="http://0.0.0.0:11434/v1",
    model_name="qwen2.5:7b-instruct",
    *args,
    **kwargs
):
    return server(
        model_type="huggingface",
        model_name=model_name,
        base_url=base_url,
        *args,
        **kwargs
    )


class HF:
    def __init__(self, model_name: HFModelType = None):
        self.model_name = model_name

    def __call__(self,
                 model_name="NousResearch/Hermes-3-Llama-3.1-8B",
                 model_type='huggingface', *args, **kwargs):
        return server(
            model_type=model_type,
            model_name=self.model_name or model_name,
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


def qwen_2_5_72b_instruct():
    return HF("Qwen/Qwen2.5-72B-Instruct")


def qwen_qwq_32b_preview():
    return HF("Qwen/QwQ-32B-Preview")


def qwen_2_5_coder_32b_instruct():
    return HF("Qwen/Qwen2.5-Coder-32B-Instruct")


def nous_hermes_3_llama_3_1_8b():
    return HF("NousResearch/Hermes-3-Llama-3.1-8B")


def microsoft_phi_3_5_mini_instruct():
    return HF("microsoft/Phi-3.5-mini-instruct")


def meta_llama_3_1_8b_instruct():
    return HF("meta-llama/Llama-3.1-8B-Instruct")


def meta_llama_3_2_1b_instruct():
    return HF("meta-llama/Llama-3.2-1B-Instruct")


def meta_llama_3_2_3b_instruct():
    return HF("meta-llama/Llama-3.2-3B-Instruct")


def yi_1_5_34b_chat():
    return HF("01-ai/Yi-1.5-34B-Chat")


def code_llama_34b_instruct_hf():
    return HF("codellama/CodeLlama-34b-Instruct-hf")


def google_gemma_1_1_7b_it():
    return HF("google/gemma-1.1-7b-it")


def google_gemma_2_2b_it():
    return HF("google/gemma-2-2b-it")


def google_gemma_2_9b_it():
    return HF("google/gemma-2-9b-it")


def google_gemma_2b_it():
    return HF("google/gemma-2b-it")


def huggingface_starchat2_15b_v0_1():
    return HF("HuggingFaceH4/starchat2-15b-v0.1")


def huggingface_zephyr_7b_alpha():
    return HF("HuggingFaceH4/zephyr-7b-alpha")


def huggingface_zephyr_7b_beta():
    return HF("HuggingFaceH4/zephyr-7b-beta")


def meta_llama_2_7b_chat_hf():
    return HF("meta-llama/Llama-2-7b-chat-hf")


def meta_llama_3_1_70b_instruct():
    return HF("meta-llama/Llama-3.1-70B-Instruct")


def meta_llama_meta_llama_3_70b_instruct():
    return HF("meta-llama/Meta-Llama-3-70B-Instruct")


def meta_llama_meta_llama_3_8b_instruct():
    return HF("meta-llama/Meta-Llama-3-8B-Instruct")


def microsoft_dialo_gpt_medium():
    return HF("microsoft/DialoGPT-medium")


def microsoft_phi_3_mini_4k_instruct():
    return HF("microsoft/Phi-3-mini-4k-instruct")


def mistralai_mistral_7b_instruct_v0_2():
    return HF("mistralai/Mistral-7B-Instruct-v0.2")


def mistralai_mistral_7b_instruct_v0_3():
    return HF("mistralai/Mistral-7B-Instruct-v0.3")


def mistralai_mixtral_8x7b_instruct_v0_1():
    return HF("mistralai/Mixtral-8x7B-Instruct-v0.1")


def nous_research_nous_hermes_2_mixtral_8x7b_dpo():
    return HF("NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")


def qwen_2_5_1_5b_instruct():
    return HF("Qwen/Qwen2.5-1.5B-Instruct")


def qwen_2_5_3b_instruct():
    return HF("Qwen/Qwen2.5-3B-Instruct")


def tiiuae_falcon_7b_instruct():
    return HF("tiiuae/falcon-7b-instruct")


def uschreiber_llama3_2():
    return HF("uschreiber/llama3.2")


def nousresearch_hermes_3_llama_3_1_8b():
    return HF("NousResearch/Hermes-3-Llama-3.1-8B")


def qwen_qwq_32b_preview():
    return HF("Qwen/QwQ-32B-Preview")

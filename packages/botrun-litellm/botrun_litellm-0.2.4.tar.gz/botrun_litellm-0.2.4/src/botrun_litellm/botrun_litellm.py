import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import litellm

__all__ = ["botrun_litellm_completion"]

load_dotenv()
version = "v0.2.2"


def get_model_config(model_name: str) -> Dict[str, str]:
    """
    Get model configuration including base URL and API key based on model prefix

    Args:
        model_name: Name of the model

    Returns:
        Dict containing model and optionally api_base and api_key
    """
    model_lower = model_name.lower()

    if model_lower.startswith("taide/"):
        # Remove 'taide/' prefix and get actual model name
        actual_model = model_name.split("/", 1)[1]
        # actual_model = model_name[6:]  # len('taide/') = 6

        taide_api_url = os.getenv("TAIDE_BASE_URL")
        taide_api_key = os.getenv("TAIDE_API_KEY")

        if not taide_api_url or not taide_api_key:
            print(
                "[botrun_litellm.py] TAIDE_BASE_URL and TAIDE_API_KEY environment variables are required for TAIDE models"
            )
            raise ValueError(
                "[botrun_litellm.py] TAIDE_BASE_URL and TAIDE_API_KEY environment variables are required for TAIDE models"
            )

        # 是 國網提供的模型 API (包含TAIDE)
        print(f"[botrun_litellm.py] using TAIDE api! {version} model={actual_model}")

        return {
            "model": actual_model,
            "base_url": taide_api_url,
            "api_key": taide_api_key,
        }

    # Handle custom botrun models
    # Format: botrun/openai/{model_name}
    if model_lower.startswith("botrun/"):
        # Remove 'taide/' prefix and get actual model name
        actual_model = model_name.split("/", 1)[1]

        base_url = os.getenv(f"BOTRUN_BASE_URL")
        api_key = os.getenv(f"BOTRUN_API_KEY")

        if not base_url or not api_key:
            raise ValueError(
                "[botrun_litellm.py] CUSTOMBOTRUM_BASE_URL and CUSTOMBOTRUM_API_KEY environment variables are required for botrun models"
            )

        # 是 botrun提供的模型 API
        print(f"[botrun_litellm.py] using botrun api! {version} model={actual_model}")

        return {
            "model": model_name,
            "base_url": base_url,
            "api_key": api_key,
            "custom_llm_provider": "openai",
        }

    # Default case - return only model name
    return {"model": model_name}


def botrun_litellm_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    stream: bool = False,
    **kwargs: Any,
) -> Any:
    """
    Enhanced wrapper for litellm.completion with support for TAIDE and custom models

    Args:
        messages: List of message dictionaries
        model: Model name (optional)
        stream: Whether to stream the response
        **kwargs: Additional arguments passed to litellm.completion

    Returns:
        litellm.completion response

    Examples:
        # Using TAIDE model
        response = botrun_litellm_completion(messages, model="taide/openai/Llama-3.1-405B-Instruct-FP8")

        # Using custom botrun model
        response = botrun_litellm_completion(messages, model="botrun/openai/gpt-4")

        # Using regular model
        response = botrun_litellm_completion(messages, model="openai/gpt-4")
    """
    model = model or os.getenv("DEFAULT_MODEL", "openai/gpt-4o-2024-08-06")

    try:
        model_config = get_model_config(model)
    except ValueError as e:
        print(f"[botrun_litellm.py] Configuration error: {str(e)}")
        raise

    completion_args = {"messages": messages, "stream": stream, **model_config, **kwargs}

    ## debug 確認參數
    # print(f"\n[botrun_litellm.py] completion_args={completion_args}")

    return litellm.completion(**completion_args)

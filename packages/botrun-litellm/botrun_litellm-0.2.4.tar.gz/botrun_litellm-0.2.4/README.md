# README.md
# botrun_litellm

A wrapper for litellm with TAIDE configuration support.

## Installation

```bash
pip install botrun_litellm
```

## Usage

```python
from botrun_litellm import botrun_litellm_completion

response = botrun_litellm_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    model="openai/gpt-4"
)
```
## Usage 2
```python
from botrun_litellm import botrun_litellm_completion

response = botrun_litellm_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    model="taide/openai/Llama3-TAIDE-LX-70B-Chat",
    api_base: "base_url",
    api_key: "api_key"

)
```


## Environment Variables

The following environment variables are required:

- `TAIDE_BASE_URL`: Base URL for TAIDE API
- `TAIDE_API_KEY`: API key for TAIDE

## Supported models
- "taide/openai/Llama-3.1-405B-Instruct-FP8",
- "taide/openai/Llama-3.1-70B",
- "taide/openai/Llama-3.1-Nemotron-70B-Instruct",
- "taide/openai/Llama3-TAIDE-LX-70B-Chat",
- "taide/openai/TAIDE-LX-70B-Chat"


## License

MIT License

# export requirements.txt
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls
```
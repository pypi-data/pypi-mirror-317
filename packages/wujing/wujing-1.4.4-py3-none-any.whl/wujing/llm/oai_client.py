from openai import OpenAI
from diskcache import FanoutCache as Cache
from typing import Optional
import os

cache = None


def validate_parameters(**params):
    validation_rules = {
        "prompt": lambda x: isinstance(x, str) and x.strip(),
        "model": lambda x: isinstance(x, str) and x.strip(),
        "api_key": lambda x: isinstance(x, str) and x.strip(),
        "api_base": lambda x: isinstance(x, str) and x.startswith("http"),
        "cache_enabled": lambda x: isinstance(x, bool),
        "cache_directory": lambda x: isinstance(x, str) and x.strip(),
    }

    for param, validator in validation_rules.items():
        if param in params and not validator(params[param]):
            raise ValueError(
                f"Invalid {param}: does not meet the required format or type."
            )


def send_req(messages, model, api_key, api_base, extra_body):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body=extra_body,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Failed to send request: {e}") from e


def to_llm(
        prompt: str,
        model: str,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        cache_enabled: bool = True,
        cache_directory: str = "./.diskcache/oai_cache",
        extra_body: object = None,
) -> str:
    global cache
    validate_parameters(
        prompt=prompt,
        model=model,
        api_key=api_key,
        api_base=api_base,
        cache_enabled=cache_enabled,
        cache_directory=cache_directory,
    )

    if cache_enabled and cache is None:
        cache = Cache(directory=cache_directory)

    # Allow API key and base URL to be configured via environment variables or function parameters
    api_key = api_key or os.getenv("OPENAI_API_KEY", "")
    api_base = api_base or os.getenv("OPENAI_API_BASE", "")

    if cache_enabled:
        cached_send_req = cache.memoize(typed=True)(send_req)
        chat_response = cached_send_req(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
            api_key=api_key,
            api_base=api_base,
            extra_body=extra_body,
        )
    else:
        chat_response = send_req(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
            api_key=api_key,
            api_base=api_base,
            extra_body=extra_body,
        )

    return chat_response


if __name__ == "__main__":
    result = to_llm(
        prompt="1+1=?",
        model="gpt-4o",
        api_key="",
        api_base="",
    )
    print(f"result:{result}")

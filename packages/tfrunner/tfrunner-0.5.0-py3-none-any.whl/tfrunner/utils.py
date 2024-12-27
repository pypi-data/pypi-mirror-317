import os
from typing import Optional


def load_env_var(var: str) -> str:
    token: Optional[str] = os.environ.get(var)
    if token is None:
        raise ValueError(f"Environment variable {var} is not set.")
    return token

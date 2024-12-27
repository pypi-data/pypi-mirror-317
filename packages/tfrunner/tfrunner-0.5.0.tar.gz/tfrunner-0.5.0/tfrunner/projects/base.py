from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel

from tfrunner.secrets_backend.base import SecretsBackendKind
from tfrunner.state_backend.base import StateBackendKind


class ProjectConfig(BaseModel):
    path: Path
    state_name: str


class SecretsBackendConfig(BaseModel):
    kind: SecretsBackendKind
    spec: dict


class StateBackendConfig(BaseModel):
    kind: StateBackendKind
    spec: dict


class TfrunnerConfig(BaseModel):
    state_backend: StateBackendConfig
    secrets_backend: SecretsBackendConfig
    projects: dict[str, ProjectConfig]

    @classmethod
    def from_yaml(cls, config_path: Path) -> Self:
        with open(config_path, "r") as f:
            config: dict = yaml.safe_load(f)
        return TfrunnerConfig(**config)

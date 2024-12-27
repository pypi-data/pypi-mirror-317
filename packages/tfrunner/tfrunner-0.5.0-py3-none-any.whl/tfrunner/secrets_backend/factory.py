from .base import SecretsBackendKind
from .gitlab import GitlabSecretsBackend, GitlabSecretsBackendSpec


class SecretsBackendFactory:
    @staticmethod
    def run(kind: SecretsBackendKind, environment: str, spec: dict) -> dict[str, str]:
        if kind == SecretsBackendKind.GITLAB:
            spec = GitlabSecretsBackendSpec(**spec)
            return GitlabSecretsBackend.run(environment, spec)
        else:
            raise ValueError(f"Unsupported secrets backend {kind}")

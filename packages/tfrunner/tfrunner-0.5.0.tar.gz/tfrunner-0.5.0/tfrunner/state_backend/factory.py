from .base import StateBackendKind
from .gitlab import GitlabStateBackend, GitlabStateBackendSpec


class StateBackendFactory:
    @staticmethod
    def run(kind: StateBackendKind, state_name: str, spec: dict) -> list[str]:
        if kind == StateBackendKind.GITLAB:
            spec = GitlabStateBackendSpec(**spec)
            return GitlabStateBackend.run(state_name, spec)
        else:
            raise ValueError(f"Unsupported state backend {kind}")

import typer

from tfrunner.utils import load_env_var

from .base import GenericStateBackend, StateBackend, StateBackendSpec


class GitlabStateBackendSpec(StateBackendSpec):
    url: str
    project_id: int
    token_var: str


class GitlabStateBackend(StateBackend):
    @staticmethod
    def _get_state_backend(
        state_name: str,
        config: GitlabStateBackendSpec,
    ) -> GenericStateBackend:
        typer.echo(
            "==> Using Gitlab terraform state backend. Initializing backend properties..."
        )
        return GenericStateBackend(
            address="{}/api/v4/projects/{}/terraform/state/{}".format(
                config.url, config.project_id, state_name
            ),
            username="dummy",
            password=load_env_var(config.token_var),
        )

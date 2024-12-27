import subprocess
from pathlib import Path
from typing import Annotated, Optional

import typer

from tfrunner.projects.base import ProjectConfig, TfrunnerConfig
from tfrunner.secrets_backend.factory import SecretsBackendFactory

app = typer.Typer()


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def apply(
    ctx: typer.Context,
    project: Annotated[
        Optional[str], typer.Option(help="name of the project to initialize")
    ],
    config_path: Annotated[
        Path,
        typer.Option(
            help="location of the config file to use for the tool's execution"
        ),
    ] = Path("tfrunner.yaml"),
) -> None:
    config = TfrunnerConfig.from_yaml(config_path)
    project_config: ProjectConfig = config.projects[project]
    _ = SecretsBackendFactory.run(
        kind=config.secrets_backend.kind,
        environment=project,
        spec=config.secrets_backend.spec,
    )
    cmds: list[str] = ["terraform", "apply"] + ctx.args
    subprocess.call(cmds, cwd=project_config.path)

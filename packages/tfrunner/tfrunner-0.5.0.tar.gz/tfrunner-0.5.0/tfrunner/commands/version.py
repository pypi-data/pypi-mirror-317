import logging
from pathlib import Path

import toml
import typer

app = typer.Typer()


@app.command()
def version() -> None:
    """show koctl version."""

    # Fetch pyproject.toml file path
    logging.info("==> Fetching pyproject file...")
    pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    logging.info(f"=> Pyproject file: {pyproject_path}")

    # Ensure file exists
    if pyproject_path.exists():
        # Load file
        logging.info("=> Parsing version...")
        pyproject_data = toml.load(pyproject_path)

        # Parse version from file
        try:
            version = pyproject_data["tool"]["poetry"]["version"]
        except KeyError as e:
            logging.error("Could not fetch version from pyproject file.")
            raise e

        # Show version in the command line
        typer.echo(f"version: {version}")
    else:
        logging.error("=> File could not be found")
        raise FileNotFoundError("Could not find package pyproject.toml file.")

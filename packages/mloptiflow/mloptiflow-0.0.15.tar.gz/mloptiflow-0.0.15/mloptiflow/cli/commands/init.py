import click
from pathlib import Path

from ..utils.config import create_project_config
from ..utils.templates import copy_template_files


ML_PARADIGMS = [
    "tabular_regression",
    "tabular_classification",
]


@click.command()
@click.argument("project_name")
@click.option(
    "--paradigm",
    type=click.Choice(ML_PARADIGMS),
    required=True,
    help="ML paradigm to use for the project",
)
@click.option(
    "--path",
    type=click.Path(),
    default=".",
    help="Path where the project should be created",
)
def init(project_name: str, paradigm: str, path: str):
    """Initialize a new ML project with the specified paradigm."""
    project_path = Path(path) / project_name
    try:
        project_path.mkdir(parents=True, exist_ok=False)
        copy_template_files(project_path, paradigm, project_name)
        create_project_config(project_path, project_name, paradigm)
        click.echo(
            f"Successfully created project '{project_name}' with {paradigm} paradigm"
        )
        click.echo(f"Project location: {project_path.absolute()}")
        click.echo("\nNext steps:")
        click.echo("1. cd " + project_name)
        click.echo("2. see README.md for more information")
    except FileExistsError:
        click.echo(f"Error: Project directory '{project_path}' already exists")

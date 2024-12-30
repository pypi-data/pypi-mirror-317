import click
from pathlib import Path
import importlib.util
import sys
from typing import Optional


@click.group()
def train():
    """Train ML models using the project's train.py script."""
    pass


@train.command()
@click.option(
    "--model-dir",
    type=click.Path(),
    default="out/models",
    help="Directory to save trained models",
)
@click.option(
    "--random-state",
    type=int,
    default=42,
    help="Random state for reproducibility",
)
def start(model_dir: Optional[str] = None, random_state: Optional[int] = None):
    """Start the training process."""
    if model_dir is None:
        model_dir = "out/models"
    if random_state is None:
        random_state = 42
    try:
        cwd = Path.cwd()
        train_script = cwd / "src" / "train.py"

        if not train_script.exists():
            raise click.ClickException(
                "train.py not found in src directory. Are you in the project root?"
            )

        spec = importlib.util.spec_from_file_location("train_module", train_script)
        module = importlib.util.module_from_spec(spec)
        sys.modules["train_module"] = module
        spec.loader.exec_module(module)

        click.echo("Starting model training...")
        module.main()
        click.echo("Training completed successfully!")

    except Exception as e:
        raise click.ClickException(str(e))

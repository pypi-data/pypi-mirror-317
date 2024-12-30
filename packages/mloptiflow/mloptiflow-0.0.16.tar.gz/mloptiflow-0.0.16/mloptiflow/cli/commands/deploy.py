import click


@click.group()
def deploy():
    """Deploy ML models to production."""
    pass


@deploy.command()
@click.argument("model_path")
@click.option(
    "--strategy",
    type=click.Choice(["canary", "blue-green", "rolling"]),
    default="canary",
    help="Deployment strategy",
)
def start(model_path: str, strategy: str):
    """Deploy a model to production."""
    click.echo(f"Deploying model from {model_path}")
    click.echo(f"Using {strategy} deployment strategy")

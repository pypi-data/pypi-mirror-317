import click


@click.group()
def monitor():
    """Monitor ML models and their performance."""
    pass


@monitor.command()
@click.argument("model_name")
def start(model_name: str):
    """Start monitoring a deployed model."""
    click.echo(f"Starting monitoring for model: {model_name}")


@monitor.command()
@click.argument("model_name")
def stop(model_name: str):
    """Stop monitoring a deployed model."""
    click.echo(f"Stopping monitoring for model: {model_name}")

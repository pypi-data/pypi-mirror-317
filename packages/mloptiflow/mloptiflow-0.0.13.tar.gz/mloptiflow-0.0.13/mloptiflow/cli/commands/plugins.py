import click


@click.group()
def plugins():
    """Manage MLOPTIFLOW plugins."""
    pass


@plugins.command()
@click.argument("plugin_name")
def install(plugin_name: str):
    """Install a plugin."""
    click.echo(f"Installing plugin: {plugin_name}")


@plugins.command()
def list():
    """List installed plugins."""
    click.echo("Installed plugins:")

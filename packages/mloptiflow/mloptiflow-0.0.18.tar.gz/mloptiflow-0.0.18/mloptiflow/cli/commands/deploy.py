import click
import subprocess
import sys
import os
from pathlib import Path
import signal
import time


@click.group()
def deploy():
    """Deploy and test ML models."""
    pass


@deploy.command()
@click.option(
    "--host",  # TODO:
    default="0.0.0.0",
    help="Host to bind the API server",
)
@click.option(
    "--port",  # TODO:
    default=8000,
    type=int,
    help="Port to bind the API server",
)
@click.option(
    "--with-api-test",
    is_flag=True,
    help="Run inference API testing script alongside the API itself",
)
def start(host: str, port: int, with_api_test: bool):
    """Start the FastAPI server and optionally run inference API testing."""
    try:
        cwd = Path.cwd()
        api_script = cwd / "api.py"
        api_test_script = cwd / "scripts" / "test_inference_api.py"

        if not api_script.exists():
            raise click.ClickException("api.py not found. Are you in the project root?")

        api_process = subprocess.Popen(
            [sys.executable, str(api_script)],
            env={**os.environ, "HOST": host, "PORT": str(port)},
        )

        click.echo(f"API server starting at http://{host}:{port}")
        click.echo("Documentation available at http://localhost:8000/docs")

        if with_api_test:
            if not api_test_script.exists():
                click.echo(
                    "Warning: test_inference_api.py not found, skipping inference API testing"
                )
            else:
                time.sleep(2)
                click.echo("\nStarting inference API testing...")
                api_test_process = subprocess.Popen(
                    [sys.executable, str(api_test_script)]
                )

        def signal_handler(signum, frame):
            click.echo("\nShutting down gracefully...")
            if with_api_test and "api_test_process" in locals():
                api_test_process.terminate()
            api_process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        api_process.wait()

    except Exception as e:
        raise click.ClickException(str(e))

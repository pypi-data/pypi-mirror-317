import pytest
import os
from click.testing import CliRunner
from pathlib import Path
from mloptiflow.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_train_command_basic(runner, temp_dir):
    """Test basic training command execution."""
    with runner.isolated_filesystem(temp_dir=temp_dir) as fs:
        result_init = runner.invoke(
            cli, ["init", "test-project", "--paradigm", "demo_tabular_classification"]
        )
        assert result_init.exit_code == 0

        project_path = Path(fs) / "test-project"
        original_dir = os.getcwd()
        try:
            os.chdir(project_path)
            result_train = runner.invoke(cli, ["train", "start"])
            assert result_train.exit_code == 0
            assert "Starting model training..." in result_train.output
            assert "Training completed successfully!" in result_train.output

            model_dir = project_path / "out" / "models"
            assert model_dir.exists()
            assert any(model_dir.glob("*_model.joblib"))

        finally:
            os.chdir(original_dir)


def test_train_command_no_project(runner, temp_dir):
    """Test training command outside of project directory."""
    with runner.isolated_filesystem(temp_dir=temp_dir):
        result_train = runner.invoke(cli, ["train", "start"])
        assert result_train.exit_code != 0
        assert "train.py not found in src directory" in result_train.output

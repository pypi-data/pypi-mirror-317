import pytest
from click.testing import CliRunner
from pathlib import Path
from mloptiflow.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_init_command_basic(runner, temp_dir):
    """Test basic project initialization with tabular_regression paradigm."""
    with runner.isolated_filesystem(temp_dir=temp_dir) as fs:
        result = runner.invoke(
            cli, ["init", "test-project", "--paradigm", "tabular_regression"]
        )

        assert result.exit_code == 0
        assert "Successfully created project 'test-project'" in result.output

        project_path = Path(fs) / "test-project"
        assert project_path.exists()
        assert (project_path / "pyproject.toml").exists()
        assert (project_path / "app.py").exists()
        assert (project_path / "mloptiflow.yaml").exists()
        assert (project_path / "test_project").exists()
        assert (project_path / "test_project" / "__init__.py").exists()

        with open(project_path / "pyproject.toml") as f:
            content = f.read()
            assert 'name = "test-project"' in content


def test_init_command_existing_directory(runner, temp_dir):
    """Test initialization when directory already exists."""
    with runner.isolated_filesystem(temp_dir=temp_dir) as fs:
        project_path = Path(fs) / "test-project"
        project_path.mkdir()

        result = runner.invoke(
            cli, ["init", "test-project", "--paradigm", "tabular_regression"]
        )

        assert result.exit_code == 0
        assert "already exists" in result.output


def test_init_command_invalid_paradigm(runner, temp_dir):
    """Test initialization with invalid paradigm."""
    with runner.isolated_filesystem(temp_dir=temp_dir):
        result = runner.invoke(cli, ["init", "test-project", "--paradigm", "invalid"])

        assert result.exit_code != 0
        assert "Invalid value for '--paradigm'" in result.output


def test_init_command_custom_path(runner, temp_dir):
    """Test initialization with custom path."""
    with runner.isolated_filesystem(temp_dir=temp_dir) as fs:
        custom_path = Path(fs) / "custom"
        custom_path.mkdir()

        result = runner.invoke(
            cli,
            [
                "init",
                "test-project",
                "--paradigm",
                "tabular_regression",
                "--path",
                str(custom_path),
            ],
        )

        assert result.exit_code == 0
        project_path = custom_path / "test-project"
        assert project_path.exists()
        assert (project_path / "test_project").exists()
        assert (project_path / "test_project" / "__init__.py").exists()


def test_init_command_hyphenated_name(runner, temp_dir):
    """Test project initialization with hyphenated name."""
    with runner.isolated_filesystem(temp_dir=temp_dir) as fs:
        result = runner.invoke(
            cli, ["init", "my-test-project", "--paradigm", "tabular_regression"]
        )

        assert result.exit_code == 0
        assert "Successfully created project 'my-test-project'" in result.output

        project_path = Path(fs) / "my-test-project"
        assert project_path.exists()
        assert (project_path / "pyproject.toml").exists()
        assert (project_path / "my_test_project").exists()
        assert (project_path / "my_test_project" / "__init__.py").exists()

        with open(project_path / "pyproject.toml") as f:
            content = f.read()
            assert 'name = "my-test-project"' in content

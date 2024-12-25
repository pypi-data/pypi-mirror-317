import pytest
from mloptiflow.cli.utils.templates import get_template_path, copy_template_files


def test_get_template_path_valid():
    """Test getting template path for valid paradigms."""
    for paradigm in ["tabular_regression", "tabular_classification"]:
        path = get_template_path(paradigm)
        assert path.exists()
        assert path.is_dir()
        assert (path / "pyproject.toml").exists()
        assert (path / "app.py").exists()


def test_get_template_path_invalid():
    """Test getting template path for invalid paradigm."""
    path = get_template_path("nonexistent_paradigm")
    assert not path.exists()


def test_copy_template_files_regression(temp_dir):
    """Test copying tabular regression template files."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_regression")

    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "app.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "Dockerfile").exists()

    assert (project_path / "src").is_dir()
    assert (project_path / "logger").is_dir()
    assert (project_path / "docs").is_dir()


def test_copy_template_files_classification(temp_dir):
    """Test copying tabular classification template files."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_classification")

    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "app.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "Dockerfile").exists()

    assert (project_path / "src").is_dir()
    assert (project_path / "logger").is_dir()
    assert (project_path / "docs").is_dir()


def test_copy_template_files_invalid_paradigm(temp_dir):
    """Test copying template files with invalid paradigm."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    with pytest.raises(ValueError, match="Template for paradigm 'invalid' not found"):
        copy_template_files(project_path, "invalid")


def test_template_file_content(temp_dir):
    """Test that copied files maintain their content."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_regression")

    with open(project_path / "pyproject.toml") as f:
        content = f.read()
        assert 'name = "test-project"' in content
        assert 'python = "^3.11"' in content
        assert 'streamlit = "^' in content

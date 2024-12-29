import pytest
from mloptiflow.cli.utils.templates import (
    get_template_path,
    copy_template_files,
    normalize_package_name,
)


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

    copy_template_files(project_path, "tabular_regression", "test_project")

    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "app.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "test_project").exists()
    assert (project_path / "test_project" / "__init__.py").exists()

    assert (project_path / "src").is_dir()
    assert (project_path / "logger").is_dir()
    assert (project_path / "docs").is_dir()


def test_copy_template_files_classification(temp_dir):
    """Test copying tabular classification template files."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_classification", "test_project")

    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "app.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "test_project").exists()
    assert (project_path / "test_project" / "__init__.py").exists()

    assert (project_path / "src").is_dir()
    assert (project_path / "logger").is_dir()
    assert (project_path / "docs").is_dir()


def test_copy_template_files_invalid_paradigm(temp_dir):
    """Test copying template files with invalid paradigm."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    with pytest.raises(ValueError, match="Template for paradigm 'invalid' not found"):
        copy_template_files(project_path, "invalid", "test_project")


def test_template_file_content(temp_dir):
    """Test that copied files maintain their content."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_regression", "test-project")

    with open(project_path / "pyproject.toml") as f:
        content = f.read()
        assert 'name = "test-project"' in content
        assert 'python = "^3.11"' in content
        assert 'streamlit = "^' in content

    assert (project_path / "test_project").exists()
    assert (project_path / "test_project" / "__init__.py").exists()


def test_normalize_package_name():
    """Test package name normalization."""
    assert normalize_package_name("project-name") == "project_name"
    assert normalize_package_name("project_name") == "project_name"
    assert normalize_package_name("projectname") == "projectname"
    assert (
        normalize_package_name("project-name-with-hyphens")
        == "project_name_with_hyphens"
    )


def test_project_with_hyphens(temp_dir):
    """Test project creation with hyphenated name."""
    project_path = temp_dir / "my-test-project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_regression", "my-test-project")

    with open(project_path / "pyproject.toml") as f:
        content = f.read()
        assert 'name = "my-test-project"' in content

    assert (project_path / "my_test_project").exists()
    assert (project_path / "my_test_project" / "__init__.py").exists()


def test_dockerfile_workdir(temp_dir):
    """Test Dockerfile WORKDIR path with hyphenated project name."""
    project_path = temp_dir / "my-test-project"
    project_path.mkdir()

    copy_template_files(project_path, "tabular_regression", "my-test-project")

    with open(project_path / "Dockerfile") as f:
        content = f.read()
        assert "WORKDIR /my-test-project" in content

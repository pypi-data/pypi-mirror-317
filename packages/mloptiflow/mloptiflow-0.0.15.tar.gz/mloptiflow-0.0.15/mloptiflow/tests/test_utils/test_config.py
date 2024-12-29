import yaml
from mloptiflow.cli.utils.config import create_project_config


def test_create_project_config_basic(temp_dir):
    """Test basic project configuration creation."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    create_project_config(project_path, "test_project", "tabular_regression")

    config_path = project_path / "mloptiflow.yaml"
    assert config_path.exists()

    with open(config_path) as f:
        config = yaml.safe_load(f)

    assert config["project_name"] == "test_project"
    assert config["paradigm"] == "tabular_regression"
    assert config["version"] == "0.0.1"


def test_create_project_config_monitoring(temp_dir):
    """Test monitoring section in project configuration."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    create_project_config(project_path, "test_project", "tabular_regression")

    with open(project_path / "mloptiflow.yaml") as f:
        config = yaml.safe_load(f)

    assert "monitoring" in config
    assert config["monitoring"]["enabled"] is False
    assert config["monitoring"]["kafka"]["bootstrap_servers"] == ["localhost:9092"]
    assert config["monitoring"]["kafka"]["topic_prefix"] == "test_project"


def test_create_project_config_deployment(temp_dir):
    """Test deployment section in project configuration."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    create_project_config(project_path, "test_project", "tabular_regression")

    with open(project_path / "mloptiflow.yaml") as f:
        config = yaml.safe_load(f)

    assert "deployment" in config
    assert config["deployment"]["strategy"] == "canary"
    assert config["deployment"]["kubernetes"]["namespace"] == "test_project"


def test_create_project_config_file_permissions(temp_dir):
    """Test that config file is created with correct permissions."""
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    create_project_config(project_path, "test_project", "tabular_regression")

    config_path = project_path / "mloptiflow.yaml"
    assert config_path.exists()
    assert oct(config_path.stat().st_mode)[-3:] in ("644", "664", "666")

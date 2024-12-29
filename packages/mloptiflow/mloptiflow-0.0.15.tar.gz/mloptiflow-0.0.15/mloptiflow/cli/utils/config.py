from pathlib import Path
import yaml


def create_project_config(project_path: Path, project_name: str, paradigm: str):
    """Create the project configuration file."""
    config = {
        "project_name": project_name,
        "paradigm": paradigm,
        "version": "0.0.1",
        "monitoring": {
            "enabled": False,
            "kafka": {
                "bootstrap_servers": ["localhost:9092"],
                "topic_prefix": project_name,
            },
        },
        "deployment": {
            "strategy": "canary",
            "kubernetes": {
                "namespace": project_name,
            },
        },
    }

    config_path = project_path / "mloptiflow.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

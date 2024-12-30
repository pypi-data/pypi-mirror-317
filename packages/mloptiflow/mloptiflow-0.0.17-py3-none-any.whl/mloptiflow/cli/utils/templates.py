import shutil
from pathlib import Path
import pkg_resources
import re
from typing import Dict


def normalize_package_name(name: str) -> str:
    """Convert project name to a valid poetry root package name."""
    return name.replace("-", "_")


def process_template_file(file_path: Path, replacements: Dict[str, str]) -> str:
    """Process a template file and replace placeholders."""
    with open(file_path, "r") as f:
        content = f.read()

    for key, value in replacements.items():
        pattern = r"\{\{\s*" + key + r"\s*\}\}"
        content = re.sub(pattern, value, content)

    return content


def create_package_directory(project_path: Path, project_name: str):
    """Create the root package directory with __init__.py."""
    package_name = normalize_package_name(project_name)
    package_dir = project_path / package_name
    package_dir.mkdir(exist_ok=True)
    (package_dir / "__init__.py").touch()


def get_template_path(paradigm: str) -> Path:
    """Get the path to the template directory for the given paradigm."""
    template_path = pkg_resources.resource_filename(
        "mloptiflow", f"templates/{paradigm}"
    )
    return Path(template_path)


def copy_template_files(project_path: Path, paradigm: str, project_name: str):
    """Copy and process template files for the given paradigm."""
    template_path = get_template_path(paradigm)

    if not template_path.exists():
        raise ValueError(f"Template for paradigm '{paradigm}' not found")

    package_name = normalize_package_name(project_name)
    replacements = {
        "project_name": project_name,
        "package_name": package_name,
    }

    create_package_directory(project_path, project_name)

    for item in template_path.glob("**/*"):
        if item.is_file():
            relative_path = item.relative_to(template_path)
            destination = project_path / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)

            if item.suffix in [".toml", ".yaml", ".yml"] or item.name == "Dockerfile":
                content = process_template_file(item, replacements)
                with open(destination, "w") as f:
                    f.write(content)
            else:
                shutil.copy2(item, destination)

import shutil
from pathlib import Path
import pkg_resources


def get_template_path(paradigm: str) -> Path:
    """Get the path to the template directory for the given paradigm."""
    template_path = pkg_resources.resource_filename(
        "mloptiflow", f"templates/{paradigm}"
    )
    return Path(template_path)


def copy_template_files(project_path: Path, paradigm: str):
    """Copy template files to the new project directory."""
    template_path = get_template_path(paradigm)

    if not template_path.exists():
        raise ValueError(f"Template for paradigm '{paradigm}' not found")

    for item in template_path.glob("**/*"):
        if item.is_file():
            relative_path = item.relative_to(template_path)
            destination = project_path / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)

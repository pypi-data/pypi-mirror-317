from pathlib import Path
from fastcraft.utils.file_writes import write_schemas_file, write_main_file
from typing_extensions import Any


def generate_file_structure(project_name: str, orm_choice: str) -> Any:
    """
    Generate a basic folder structure for a FastAPI project, considering cross-platform compatibility.
    """
    base_dir = Path.cwd() / project_name

    # Define the folder structure
    folders = ["app", "app/routers", "app/models", "app/core", "app/utils", "tests"]

    # If ORM choice given by the user is SQLAlchemy, include the shemas folder in the scaffold
    if orm_choice == "sqlalchemy":
        folders.append("app/schemas")

    # Create the directories
    for folder in folders:
        dir_path = base_dir / folder
        dir_path.mkdir(parents=True, exist_ok=True)

    # prefill the schemas.py with some useful information
    if orm_choice == "sqlalchemy":
        write_schemas_file(project_name)

    # Create a basic main.py file
    write_main_file(project_name)

from pathlib import Path
import os

def generate_basic_structure(projectname: str):
    """
    Generate a basic folder structure for a FastAPI project, considering cross-platform compatibility.
    """
    base_dir = Path.cwd() / projectname

    # Define the folder structure
    folders = [
        "app",
        "app/routers",
        "app/models",
        "app/schemas",
        "app/core",
        "app/utils",
        "tests"
    ]

    # Create the directories
    for folder in folders:
        dir_path = base_dir / folder
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create a basic main.py file
    main_file_path = base_dir / "app" / "main.py"
    main_file_path.write_text(
        """from fastapi import FastAPI\n\n"""
        """app = FastAPI()\n\n"""
        """@app.get("/")\n"""
        """def read_root():\n"""
        """    return {"message": "Hello, FastForge!"}\n""",
        encoding="utf-8"
    )

    print(f"✅ Basic FastAPI project '{projectname}' has been created at {base_dir}")

import subprocess
from rich import print
from pathlib import Path
import typer
from typing import Dict, List

# Define package dependencies for each ORM and database
DEPENDENCIES: Dict[str, Dict[str, List[str]]] = {
    "orm": {
        "sqlalchemy": ["fastapi", "sqlalchemy", "alembic", "python-dotenv"],
        "sqlmodel": ["fastapi", "sqlmodel", "alembic", "python-dotenv"],
        "tortoiseorm": ["fastapi", "tortoise-orm", "aerich", "python-dotenv"],
    },
    "database": {
        "postgresql": ["psycopg2-binary"],
        "sqlite": [],  # SQLite comes with Python standard library
        "mongodb": ["motor", "odmantic"],
    },
    "core": ["uvicorn", "python-multipart", "pydantic-settings", "pydantic[email]"],
    "dev": ["ruff", "pytest"],
}


def initialize_packages(
    project_name: str, orm_choice: str, database_choice: str
) -> None:
    """
    Initialize a FastAPI project with the selected ORM and database dependencies.

    Args:
        project_name: Name of the project directory
        orm_choice: Selected ORM (sqlalchemy, sqlmodel, or tortoiseorm)
        database_choice: Selected database (postgres, mysql, sqlite, or mongodb)
    """
    project_path = Path(project_name)

    try:
        # Initialize uv environment
        print("\n[blue]📦 Initializing uv environment...[/blue]")
        subprocess.run(["uv", "init"], check=True, cwd=project_path)

        # Get production dependencies
        prod_packages = (
            DEPENDENCIES["core"]
            + DEPENDENCIES["orm"].get(orm_choice, [])
            + DEPENDENCIES["database"].get(database_choice, [])
        )

        # Get development dependencies
        dev_packages = DEPENDENCIES["dev"]

        # Install production dependencies
        if prod_packages:
            print(
                f"\n[blue]📥 Installing dependencies for {orm_choice} with {database_choice}...[/blue]"
            )
            subprocess.run(["uv", "add"] + prod_packages, check=True, cwd=project_path)

        # Install development dependencies
        if dev_packages:
            print("\n[blue]📥 Installing development dependencies...[/blue]")
            subprocess.run(
                ["uv", "add", "--dev"] + dev_packages, check=True, cwd=project_path
            )

        # Print summary of installed packages
        print("\n[green]✅ Dependencies installed successfully![/green]")
        print("\n[blue]📚 Production packages:[/blue]")
        for package in prod_packages:
            print(f"  • {package}")

        print("\n[blue]📚 Development packages:[/blue]")
        for package in dev_packages:
            print(f"  • {package}")

    except subprocess.CalledProcessError as e:
        print(f"[red]❌ Error during dependency installation: {e}[/red]")
        # Print more detailed error information
        if e.stderr:
            print(f"[red]Error details: {e.stderr.decode()}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"[red]❌ Unexpected error: {str(e)}[/red]")
        raise typer.Exit(code=1)

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn
from pathlib import Path
from fastcraft.utils.generate_file_struct import generate_file_structure
from fastcraft.utils.choices import get_orm_choice, get_database_choice
from fastcraft.utils.package_manager import initialize_packages
from typing_extensions import Annotated, Any


create_dir = typer.Typer()


@create_dir.command()
def init(
    project_name: Annotated[str, typer.Argument(help="Start a new FastAPI Project")],
) -> Any:
    """
    Start a new FastAPI project
    """
    base_dir = Path.cwd() / project_name

    if base_dir.exists():
        print(
            f"[red]❌ Error: A project named '{project_name}' already exists in the current directory.[/red]"
        )
        raise typer.Exit(code=1)

    orm_choice = get_orm_choice()
    database_choice = get_database_choice()
    steps = [
        (
            lambda: generate_file_structure(
                project_name,
                orm_choice,
            )
        ),
        (lambda: initialize_packages(project_name, orm_choice, database_choice)),
    ]
    with Progress(SpinnerColumn(spinner_name="aesthetic"), transient=True) as progress:
        for task_func in steps:
            progress_task = progress.add_task(
                "", total=None
            )  # No description, just the spinner
            task_func()
            progress.remove_task(progress_task)

    print(f"\n✅ FastAPI project '{project_name}' has been created at {base_dir}")
    print(f"🎉 Project '{project_name}' is ready!")

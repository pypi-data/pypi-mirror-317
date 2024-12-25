import typer
from fastcraft.utils.generate_file_struct import generate_file_structure


create_dir = typer.Typer()


@create_dir.command()
def init(projectname: str):
    """
    Start a new FastAPI project 
    """
    print(f"🚀 Starting new project: {projectname}")
    generate_file_structure(projectname)
    print(f"🎉 Project '{projectname}' is ready!")

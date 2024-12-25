import typer
from fastcraft.directory.create_dir import generate_basic_structure


app = typer.Typer()

@app.command('start')
def initiate_project_setup(projectname: str):
    """
    Start a new FastAPI project with a basic folder structure.
    """
    print(f"🚀 Starting new project: {projectname}")
    generate_basic_structure(projectname)
    print(f"🎉 Project '{projectname}' is ready!")

if __name__ == "__main__":
    app()
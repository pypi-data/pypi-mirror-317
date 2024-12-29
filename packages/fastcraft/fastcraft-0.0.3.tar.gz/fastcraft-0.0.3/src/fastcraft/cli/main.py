import typer
from .create_dir import create_dir as create_dir_app

cli_app = typer.Typer()

cli_app.add_typer(create_dir_app)

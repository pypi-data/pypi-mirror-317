from InquirerPy import inquirer


def get_orm_choice():
    """
    Prompt the user to select the database ORM to use.
    Returns:
        str: The selected ORM (e.g., 'sqlalchemy', 'sqlmodel').
    """
    return inquirer.select(
        message="Select the database ORM/ODM to use:",
        choices=[
            {"name": "SQLModel", "value": "sqlmodel"},
            {"name": "SQLAlchemy", "value": "sqlalchemy"},
            {"name": "TortoiseORM", "value": "tortoiseorm"},
            {"name": "Beanie", "value": "beanie"},
        ],
        default="sqlmodel",
    ).execute()


def get_database_choice():
    """
    Prompt the user to select the database ORM to use.
    Returns:
        str: The selected ORM (e.g., 'sqlalchemy', 'sqlmodel').
    """

    return inquirer.select(
        message="Select the database to use:",
        choices=[
            {"name": "SQLite", "value": "sqlite"},
            {"name": "PostgreSQL", "value": "postgresql"},
            {"name": "MongoDB", "value": "mongodb"},
        ],
        default="sqlite",
    ).execute()

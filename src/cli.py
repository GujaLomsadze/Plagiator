import os
import questionary
from rich.console import Console
from dotenv import load_dotenv
from main import main

console = Console()


def choose_env_or_manual():
    """Ask user whether to use .env or manual input"""
    choice = questionary.select(
        "How do you want to provide database connection details?",
        choices=[
            "Load from .env file",
            "Enter manually in CLI"
        ]
    ).ask()
    return choice


def choose_env_file(default: str = ".env"):
    """Prompt user to choose .env file"""
    while True:
        env_file = questionary.path("Select your .env file:", default=default).ask()
        if env_file and os.path.isfile(env_file):
            load_dotenv(env_file)
            console.print(f"[green]Loaded environment from: {env_file}[/green]")
            return os.path.abspath(env_file)
        console.print("[red]Invalid file. Please try again.[/red]")


def enter_db_details_manually():
    """Prompt user for DB connection details and set as env vars"""
    os.environ["DB_HOST"] = questionary.text("Database Host:", default="localhost").ask()
    os.environ["DB_PORT"] = questionary.text("Database Port:", default="5432").ask()
    os.environ["DB_USER"] = questionary.text("Database User:", default="postgres").ask()
    os.environ["DB_PASSWORD"] = questionary.password("Database Password:").ask()
    os.environ["DB_NAME"] = questionary.text("Target Database Name:", default="postgres").ask()

    console.print("\n[green]Database details stored in memory for this session.[/green]")


def choose_sql_folder(default: str = "../sql_scripts"):
    """Prompt user to select SQL scripts folder"""
    while True:
        folder = questionary.path("Select SQL scripts folder:", default=default).ask()
        if folder and os.path.isdir(folder):
            return os.path.abspath(folder)
        console.print("[red]Invalid folder. Please try again.[/red]")


def run_cli():
    console.print("[bold cyan]🚀 Database Reset & Initialization Tool[/bold cyan]\n")

    # Step 1: Choose connection method
    method = choose_env_or_manual()
    if method == "Load from .env file":
        env_file = choose_env_file()
    else:
        enter_db_details_manually()

    # Step 2: Choose SQL folder
    sql_folder = choose_sql_folder()

    # Step 3: Show summary
    console.print("\n[bold yellow]Summary:[/bold yellow]")
    console.print(f"• DB Host: [cyan]{os.getenv('DB_HOST')}[/cyan]")
    console.print(f"• DB User: [cyan]{os.getenv('DB_USER')}[/cyan]")
    console.print(f"• Target DB: [cyan]{os.getenv('DB_NAME')}[/cyan]")
    console.print(f"• SQL folder: [cyan]{sql_folder}[/cyan]\n")

    # Step 4: Confirm
    confirm = questionary.confirm(
        "⚠️ This will DROP and recreate the target database. Proceed?"
    ).ask()
    if not confirm:
        console.print("[red]Operation canceled.[/red]")
        return

    # Step 5: Run the database reset and initialization
    main(sql_scripts_path=sql_folder)


if __name__ == "__main__":
    run_cli()

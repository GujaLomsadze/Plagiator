import os
import questionary
from rich.console import Console
from main import main

console = Console()


def choose_folder(prompt_text: str, default: str = None):
    """Prompt user to choose a folder interactively."""
    while True:
        folder = questionary.path(prompt_text, default=default).ask()
        if folder and os.path.isdir(folder):
            return os.path.abspath(folder)
        console.print("[red]Invalid folder. Please try again.[/red]")


def choose_env_file(default: str = ".env"):
    """Prompt user to choose .env file"""
    while True:
        env_file = questionary.path("Select your .env file:", default=default).ask()
        if env_file and os.path.isfile(env_file):
            console.print(f"[green]Selected env file: {env_file}[/green]")
            return os.path.abspath(env_file)
        console.print("[red]Invalid file. Please try again.[/red]")


def run_cli():
    console.print("[bold cyan]🚀 Database Reset & Initialization Tool[/bold cyan]\n")

    env_file = choose_env_file()
    os.environ['DOTENV_PATH'] = env_file  # optionally store

    sql_folder = choose_folder("Select your SQL scripts folder:", "../sql_scripts")

    console.print("\n[bold yellow]Summary:[/bold yellow]")
    console.print(f"• Env file: [cyan]{env_file}[/cyan]")
    console.print(f"• SQL scripts folder: [cyan]{sql_folder}[/cyan]\n")

    confirm = questionary.confirm("Proceed with resetting and initializing the database?").ask()
    if not confirm:
        console.print("[red]Operation canceled.[/red]")
        return

    # Run main.py with the selected SQL folder
    main(sql_scripts_path=sql_folder)


if __name__ == "__main__":
    run_cli()

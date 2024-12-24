import subprocess
import time
from getpass import getpass

import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .auth import save_credentials, validate_credentials

console = Console()

ARCADIA_ASCII = r"""
[bold cyan]
    ___    ____  ____  ___    ____  ____  ___   
   /   |  / __ \/ ___//   |  / __ \/  _/ /   |  
  / /| | / /_/ / /   / /| | / / / // /  / /| |  
 / ___ |/ _, _/ /___/ ___ |/ /_/ // /  / ___ |  
/_/  |_/_/ |_|\____/_/  |_/_____/___/ /_/  |_|  
[/bold cyan]
[italic blue]🚀 Welcome to the Arcadia AI SDK - Deploy models at the speed of thought[/italic blue]
"""


def show_welcome():
    console.print(Panel(ARCADIA_ASCII, border_style="cyan"))
    console.print("\n[dim]Version 0.1.0 | © 2024 Arcadia AI[/dim]\n")


@click.group()
def cli():
    """Arcadia CLI tool"""
    pass


@cli.command()
@click.argument("model_name", required=True)
@click.option("--description", "-d", help="Model description")
@click.option("--gpu/--no-gpu", default=True, help="Whether the model requires GPU")
def deploy(model_name: str, description: str = None, gpu: bool = True):
    """Deploy a model to Arcadia

    MODEL_NAME is the name for your model
    """
    from arcadia import ArcadiaClient

    client = ArcadiaClient()
    client.deploy(model_name=model_name, description=description, gpu=gpu)


@cli.command()
def login():
    """Log in to Arcadia"""
    show_welcome()

    console.print("[bold blue]🔐 Authentication Required[/bold blue]")
    console.print("Please enter your Arcadia credentials to continue.\n")

    username = console.input("[cyan]Username: [/cyan]")
    api_key = getpass("API Key: ")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[cyan]Validating credentials...", total=None)
        time.sleep(1)  # Add a small delay for better UX

        if validate_credentials(username, api_key):
            save_credentials(username, api_key)
            console.print("\n[green]✓[/green] Authentication successful!\n")

            # Show some helpful next steps
            console.print(
                Panel.fit(
                    "[bold green]🎉 Welcome to Arcadia![/bold green]\n\n"
                    "You're now ready to use the Arcadia SDK. Here are some things you can try:\n\n"
                    "[cyan]• Deploy a model:[/cyan] arcadia deploy\n"
                    "[cyan]• Check status:[/cyan] arcadia status\n"
                    "[cyan]• View documentation:[/cyan] arcadia docs\n\n"
                    "For more information, visit [link]https://docs.arcadia.ai[/link]",
                    title="Getting Started",
                    border_style="green",
                )
            )
        else:
            console.print("\n[red]✗ Authentication failed![/red]")
            console.print(
                "[yellow]Please check your credentials and try again.[/yellow]\n"
                "If you need help, visit [link]https://support.arcadia.ai[/link]"
            )


@cli.command()
def version():
    """Show version information"""
    console.print("[cyan]Arcadia SDK[/cyan] version 0.1.0")


if __name__ == "__main__":
    cli()

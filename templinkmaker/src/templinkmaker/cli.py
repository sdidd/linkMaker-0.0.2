"""Console script for templinkmaker."""
import templinkmaker

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for templinkmaker."""
    console.print("Replace this message by putting your code into "
               "templinkmaker.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()

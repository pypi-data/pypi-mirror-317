from rich.text import Text
from rich.console import Console


def show_help():
    console = Console()
    help_text = Text("\n Soon I will write documentation for this script here\n", style="bold green")
    help_text.append(" For now you can get help at my telegram ", style="bold green")
    help_text.append(" https://t.me/BugScanX", style="bold blue underline")
    console.print(help_text)



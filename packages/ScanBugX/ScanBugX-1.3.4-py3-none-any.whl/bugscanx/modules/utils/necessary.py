import os
import pyfiglet
from rich.text import Text
from rich.console import Console


def text_ascii(text, font="doom", color="white", shift=2):
    try:
        ascii_banner = pyfiglet.figlet_format(text, font=font)
        shifted_banner = "\n".join((" " * shift) + line for line in ascii_banner.splitlines())
        banner_text = Text(shifted_banner, style=color)
        console = Console()
        console.print(banner_text)
    except pyfiglet.FontNotFound:
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


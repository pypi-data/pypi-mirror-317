import sys
import subprocess
import pyfiglet
from rich.text import Text
from rich.console import Console


def install_requirements():
    required_packages = {
        'requests': 'requests',
        'rich': 'rich',
        'colorama': 'colorama',
        'ipaddress': 'ipaddress',
        'pyfiglet': 'pyfiglet',
        'ssl': 'ssl',
        'beautifulsoup4': 'bs4',
        'dnspython': 'dns',
        'multithreading': 'multithreading',
        'loguru': 'loguru'
    }
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"\033[33m Package '{package}' is not installed. Installing...\033[0m")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\033[32m Package '{package}' installed successfully.\033[0m")

def text_ascii(text, font="doom", color="white", shift=2):
    try:
        ascii_banner = pyfiglet.figlet_format(text, font=font)
        shifted_banner = "\n".join((" " * shift) + line for line in ascii_banner.splitlines())
        banner_text = Text(shifted_banner, style=color)
        console = Console()
        console.print(banner_text)
    except pyfiglet.FontNotFound:
        pass
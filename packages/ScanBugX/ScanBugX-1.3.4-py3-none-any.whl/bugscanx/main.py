import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
install_requirements()

from rich.console import Console
from bugscanx.modules.utils.other import banner
from bugscanx.modules.utils.handler import *
from bugscanx.modules.utils.glance import display_message
from bugscanx.modules.utils.necessary import text_ascii, clear_screen
console = Console()

def get_input(prompt, default=None):
    if default:
        full_prompt = f"[cyan]{prompt}[/cyan] [dim white][{default}][/dim white]: "
    else:
        full_prompt = f"[cyan]{prompt}[/cyan]: "
    response = console.input(full_prompt)
    if response is None:
        return default
    response = response.strip()
    return response if response else default

def main_menu():
    while True:
        clear_screen()
        banner()
        display_message()
        console.print("[bold cyan]\n [1]  Host Scanner(pro)")
        console.print("[bold green] [2]  Host scanner")
        console.print("[bold yellow] [3]  CIDR Scanner")
        console.print("[bold magenta] [4]  Subdomains Finder")
        console.print("[bold yellow] [5]  Reverse IP Lookup")
        console.print("[bold blue] [6]  TXT Toolkit")
        console.print("[bold green] [7]  Open Port Checker")
        console.print("[bold bright_magenta] [8]  DNS Records")
        console.print("[bold cyan] [9]  OSINT")
        console.print("[bold bright_yellow] [10] Help")
        console.print("[bold red] [11] Exit\n")

        choice = get_input(" Enter your choice")
        options = {
            '1': ("HOST SCANNER", run_host_checker),
            '2': ("SUB SCANNER", run_sub_scan),
            '3': ("CIDR SCANNER", run_ip_scan),
            '4': ("SUBFINDER", run_sub_finder),
            '5': ("IP LOOKUP", run_ip_lookup),
            '6': ("TxT TOOLKIT", run_txt_toolkit),
            '7': ("OPEN PORT", run_open_port),
            '8': ("DNS RECORDS", run_dns_info),
            '9': ("OSINT", run_osint),
            '10': ("HELP MENU", run_help_menu),
            '11': ("EXIT", lambda: sys.exit())
        }

        if choice in options:
            clear_screen()
            text_ascii(options[choice][0], font="calvin_s", color="bold magenta")
            options[choice][1]()
            if choice != '11':
                console.input("[yellow]\n Press Enter to return to the main menu...")
        else:
            console.print("[bold red]\n Invalid choice. Please select a valid option.")
            console.input("[yellow bold]\n Press Enter to return to the main menu...")

if __name__ == "__main__":
    main_menu()

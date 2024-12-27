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

import pyfiglet
from rich.text import Text
from rich.console import Console
from bugscanx.modules.utils.other import banner
from bugscanx.modules.utils.handler import *
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def text_to_ascii_banner(text, font="doom", color="white", shift=2):
    try:
        ascii_banner = pyfiglet.figlet_format(text, font=font)
        shifted_banner = "\n".join((" " * shift) + line for line in ascii_banner.splitlines())
        banner_text = Text(shifted_banner, style=color)
        console = Console()
        console.print(banner_text)
    except pyfiglet.FontNotFound:
        pass

def main_menu():
    while True:
        clear_screen()
        banner()
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

        if choice == '1':
            clear_screen()
            text_to_ascii_banner("HOST SCANNER", font="calvin_s", color="bold magenta")
            run_host_checker()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "2":
            clear_screen()
            text_to_ascii_banner("SUB SCANNER", font="calvin_s", color="bold magenta")
            run_sub_scan()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            text_to_ascii_banner("CIDR SCANNER", font="calvin_s", color="bold magenta")
            run_ip_scan()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            text_to_ascii_banner("SUBFINDER", font="calvin_s", color="bold magenta")
            run_sub_finder()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "5":
            clear_screen()
            text_to_ascii_banner("IP LOOKUP", font="calvin_s", color="bold magenta")
            run_ip_lookup()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice =="6":
            clear_screen()
            text_to_ascii_banner("TxT TOOLKIT", font="calvin_s", color="bold magenta")
            run_txt_toolkit()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "7":
            clear_screen()
            text_to_ascii_banner("OPEN PORT", font="calvin_s", color="bold magenta")
            run_open_port()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "8":
            clear_screen()
            text_to_ascii_banner("DNS RECORDS", font="calvin_s", color="bold magenta")
            run_dns_info()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "9":
            clear_screen()
            text_to_ascii_banner("OSINT", font="calvin_s", color="bold magenta")
            run_osint()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "10":
            clear_screen()
            text_to_ascii_banner("HELP MENU", font="calvin_s", color="bold magenta")
            run_help_menu()
            console.input("[yellow]\n Press Enter to return to the main menu...")

        elif choice == "11":
            console.print("[bold red]\n Shutting down the toolkit. See you next time!")
            sys.exit()

        else:
            console.print("[bold red]\n Invalid choice. Please select a valid option.")
            console.input("[yellow bold]\n Press Enter to return to the main menu...")

if __name__ == "__main__":
    main_menu()

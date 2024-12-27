import os
from rich.console import Console
console = Console()

SUBSCAN_TIMEOUT = 5
SUBFINDER_TIMEOUT = 10

EXCLUDE_LOCATIONS = ["https://jio.com/BalanceExhaust", "http://filter.ncell.com.np/nc"]

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

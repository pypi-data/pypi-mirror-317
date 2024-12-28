import os
import time
import requests
import ipaddress
import threading
from pathlib import Path
from rich.console import Console
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from bugscanx.modules.utils.utils import get_input,clear_screen,SUBSCAN_TIMEOUT,EXCLUDE_LOCATIONS
from bugscanx.modules.scanners.sub_scan import file_manager

file_write_lock = threading.Lock()

console = Console()

def get_cidrs_from_file(file_path):
    invalid_attempts = 0
    while True:
        try:
            with open(file_path, 'r') as file:
                cidr_list = [line.strip() for line in file if line.strip()]
                ip_list = []
                for cidr in cidr_list:
                    try:
                        network = ipaddress.ip_network(cidr, strict=False)
                        ip_list.extend([str(ip) for ip in network.hosts()])
                    except ValueError as e:
                        console.print(f"[red] Invalid CIDR '{cidr}': {e}[/red]")
                return ip_list
        except Exception as e:
            console.print(f"[red] Error reading file: {e}[/red]")
            invalid_attempts += 1

        if invalid_attempts >= 3:
            console.print("[red] Too many invalid attempts. Returning to main menu.[/red]")
            time.sleep(1)
            return []

def get_cidrs_from_input():
    invalid_attempts = 0
    while True:
        cidr_input = get_input(" Enter CIDR blocks or individual IPs (comma-separated)")
        if not cidr_input:
            console.print(" No input provided. Please enter valid CIDRs or IPs.")
            invalid_attempts += 1
        else:
            cidr_list = [cidr.strip() for cidr in cidr_input.split(',')]
            ip_list = []
            for cidr in cidr_list:
                try:
                    network = ipaddress.ip_network(cidr, strict=False)
                    ip_list.extend([str(ip) for ip in network.hosts()])
                except ValueError:
                    console.print(f"[red] Invalid CIDR '{cidr}'. Skipping...[/red]")
            return ip_list

        if invalid_attempts >= 3:
            console.print("[red] Too many invalid attempts. Returning to main menu.[/red]")
            time.sleep(1)
            return []

def get_http_method():
    methods = ['GET', 'POST', 'PATCH', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'HEAD']
    console.print(f"[cyan]🌐 Available HTTP methods: {', '.join(methods)}[/cyan]")
    method = get_input(" Select an HTTP method","HEAD").upper()
    return method if method in methods else "HEAD"

def get2_scan_inputs():
    invalid_attempts = 0
    hosts = []

    while True:
        input_choice = get_input("\n Would you like to input CIDRs manually or from a file? (M/F)").lower()
        
        if input_choice == 'f':
            selected_file = file_manager(Path.cwd(), max_up_levels=3)
            
            if selected_file:
                hosts = get_cidrs_from_file(selected_file)
                if hosts:
                    break
                else:
                    console.print("[red] No valid IPs found in the CIDR file. Please try again.[/red]")
                    invalid_attempts += 1
            else:
                invalid_attempts += 1
                console.print("[red] No file selected or too many invalid attempts.[/red]")

        elif input_choice == 'm':
            hosts = get_cidrs_from_input()
            if hosts:
                break  # Break out of the loop after manual input
            else:
                console.print("[red] No valid IPs provided in manual input.[/red]")
                invalid_attempts += 1

        else:
            console.print("[red] Invalid choice. Please select 'M' for manual or 'F' for file.[/red]")
            invalid_attempts += 1

        if invalid_attempts >= 3:
            console.print("[red] Too many invalid attempts. Returning to main menu.[/red]")
            time.sleep(1)
            return None, None, None, None, None

    ports_input = get_input(" Enter port list","80")
    ports = ports_input.split(',') if ports_input else ["80"]

    output_file = get_input(" Enter output file name")
    if not output_file:
        output_file = "scan_results.txt"

    while True:
        threads_input = get_input(" Enter number of threads", "50")
        if not threads_input:
            threads = 50
            break
        try:
            threads = int(threads_input)
            if threads <= 0:
                console.print("[red] Please enter a positive integer for the number of threads.[/red]")
                continue
            break
        except ValueError:
            console.print("[red] Invalid input. Please enter a valid integer for the number of threads.[/red]")
            
    http_method = get_http_method()  

    return hosts, ports, output_file, threads, http_method

def format_row(code, server, port, host, use_colors=True):
    if use_colors:
        return (Fore.GREEN + f"{code:<4} " +
                Fore.CYAN + f"{server:<20} " +
                Fore.YELLOW + f"{port:<5} " +
                Fore.LIGHTBLUE_EX + f"{host}")
    else:
        return f"{code:<4} {server:<20} {port:<5} {host}"

def check_http_response(host, port, method):
    protocol = "https" if port in ['443', '8443'] else "http"
    url = f"{protocol}://{host}:{port}"
    try:
        response = requests.request(method, url, timeout=SUBSCAN_TIMEOUT, allow_redirects=True)
        location = response.headers.get('Location', '')
        if any(exclude in location for exclude in EXCLUDE_LOCATIONS):
            return None
        server_header = response.headers.get('Server', 'N/A')
        return response.status_code, server_header, port, host
    except requests.exceptions.RequestException:
        return None

def perform2_scan(hosts, ports, output_file, threads, method):
    clear_screen()
    print(Fore.GREEN + f"🔍 Scanning using HTTP method: {method}...")

    headers = (Fore.GREEN + "Code  " + Fore.CYAN + "Server               " +
               Fore.YELLOW + "Port   " + Fore.LIGHTBLUE_EX + "Host" + Style.RESET_ALL)
    separator = "----  ----------------   ----  -------------------------"

    existing_lines = 0
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_lines = sum(1 for _ in file)

    with open(output_file, 'a') as file:
        if existing_lines == 0:
            file.write(headers + "\n")
            file.write(separator + "\n")

    print(headers)
    print(separator)

    total_hosts = len(hosts) * len(ports)
    scanned_hosts = 0
    responded_hosts = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for host in hosts:
            for port in ports:
                futures.append(executor.submit(check_http_response, host, port, method))

        for future in as_completed(futures):
            result = future.result()
            scanned_hosts += 1

            if result:
                responded_hosts += 1
                code, server, port, host = result
                result_row = format_row(code, server, port, host)

                print(result_row)
                with open(output_file, 'a') as file:
                    file.write(format_row(code, server, port, host, use_colors=False) + "\n")

            progress_line = (Fore.YELLOW +
                             f"Scanned {scanned_hosts}/{total_hosts} - Responded: {responded_hosts}")
            print(progress_line, end='\r')

    print(f"\n\n{Fore.GREEN} Scan completed! Results saved to {output_file}.")

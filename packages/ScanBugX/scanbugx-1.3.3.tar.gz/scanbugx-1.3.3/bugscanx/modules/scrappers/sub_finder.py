import re
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from bugscanx.modules.utils.http_utils import HEADERS, USER_AGENTS
from bugscanx.modules.utils.utils import get_input, SUBFINDER_TIMEOUT
from rich.console import Console

session = requests.Session()
console = Console()

def get_random_headers():
    headers = HEADERS.copy()
    headers["user-agent"] = random.choice(USER_AGENTS)
    return headers

def fetch_subdomains(source_func, domain):
    try:
        subdomains = source_func(domain)
        return set(sub for sub in subdomains if isinstance(sub, str))
    except Exception:
        return set()

def crtsh_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://crt.sh/?q=%25.{domain}&output=json", headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200 and response.headers.get('Content-Type') == 'application/json':
        for entry in response.json():
            subdomains.update(entry['name_value'].splitlines())
    return subdomains

def hackertarget_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200 and 'text' in response.headers.get('Content-Type', ''):
        subdomains.update([line.split(",")[0] for line in response.text.splitlines()])
    return subdomains

def rapiddns_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://rapiddns.io/subdomain/{domain}?full=1", headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('td'):
            text = link.get_text(strip=True)
            if text.endswith(f".{domain}"):
                subdomains.add(text)
    return subdomains

def anubisdb_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://jldc.me/anubis/subdomains/{domain}", headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200:
        subdomains.update(response.json())
    return subdomains

def alienvault_subdomains(domain):
    subdomains = set()
    response = session.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200:
        for entry in response.json().get("passive_dns", []):
            subdomains.add(entry.get("hostname"))
    return subdomains

def urlscan_subdomains(domain):
    subdomains = set()
    url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    response = session.get(url, headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        for result in data.get('results', []):
            page_url = result.get('page', {}).get('domain')
            if page_url and page_url.endswith(f".{domain}"):
                subdomains.add(page_url)
    return subdomains

recently_seen_subdomains = set()

def c99_subdomains(domain, days=10):
    base_url = "https://subdomainfinder.c99.nl/scans"
    subdomains = set()
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
    urls = [f"{base_url}/{date}/{domain}" for date in dates]

    def fetch_url(url):
        try:
            response = session.get(url, headers=get_random_headers(), timeout=SUBFINDER_TIMEOUT)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    if text.endswith(f".{domain}") and text not in recently_seen_subdomains:
                        subdomains.add(text)
                        recently_seen_subdomains.add(text)
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in as_completed(futures):
            future.result()

    return subdomains

def is_valid_domain(domain):
    regex = re.compile(
        r'^(?:[a-zA-Z0-9]'
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'
        r'+[a-zA-Z]{2,6}$'
    )
    return re.match(regex, domain) is not None

def process_domain(domain, output_file, sources):
    if not is_valid_domain(domain):
        console.print(f"\n Invalid domain: {domain}", style="bold red")
        return

    console.print(f" Enumerating {domain}\n", style="bold cyan")
    
    subdomains = set()

    with ThreadPoolExecutor(max_workers=min(len(sources), 10)) as executor:
        futures = {executor.submit(fetch_subdomains, source, domain): source for source in sources}
        for future in as_completed(futures):
            subdomains.update(future.result())

    console.print(f"\n Completed {domain} - {len(subdomains)} subdomains found", style="bold green")
    
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"\n# Subdomains for {domain}\n")
        for subdomain in sorted(subdomains):
            if is_valid_domain(subdomain):
                file.write(f"{subdomain}\n")

def find_subdomains():
    input_choice = get_input("\n Enter 1 for single domain or 2 for txt file")
    
    if input_choice == '1':
        domain = get_input(" Enter the domain to find subdomains for")
        if not domain:
            console.print(" Domain cannot be empty.", style="bold red")
            return
        domains_to_process = [domain]
        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains, c99_subdomains
        ]
        
    elif input_choice == '2':
        file_path = get_input(" Enter the path to the file containing domains")
        try:
            with open(file_path, 'r') as file:
                domains_to_process = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            console.print(" File not found. Please check the path.", style="bold red")
            return

        sources = [
            crtsh_subdomains, hackertarget_subdomains, rapiddns_subdomains,
            anubisdb_subdomains, alienvault_subdomains,
            urlscan_subdomains
        ]
    
    else:
        console.print(" Invalid choice.", style="bold red")
        return

    output_file = get_input(" Enter the output file name (without extension)")
    if not output_file:
        console.print(" Output file name cannot be empty.", style="bold red")
        return
    output_file = output_file + "_subdomains.txt"

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_domain, domain, output_file, sources): domain for domain in domains_to_process}
        for future in as_completed(futures):
            future.result()

    console.print(f" All results saved to {output_file}", style="bold green")

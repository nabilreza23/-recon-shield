import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import concurrent.futures
import re
from urllib.parse import urljoin, urlparse

init(autoreset=True)

# Extended High-Risk Wordlist for Hidden Paths, Admins, & Sensitive Leaks
HIGH_RISK_PATHS = [
    # Admins & Dashboards
    'admin/', 'administrator/', 'admin/login.php', 'cpanel', 'phpmyadmin/', 
    'dashboard/', 'wp-admin/', 'user/login', 'controlpanel/', 'backend/',
    
    # Sensitive Files & Leaks
    '.env', '.git/HEAD', '.git/config', '.htaccess', '.vscode/sftp.json',
    'config.php', 'configuration.php', 'settings.py', 'database.yml',
    
    # Backups & Logs
    'backup.zip', 'backup.tar.gz', 'db.sql', 'database.sql', 'dump.sql',
    'error.log', 'debug.log', 'app.log', 'config.php.bak',
    
    # Endpoints & Specs
    'api/', 'v1/', 'v2/', 'swagger.json', 'api-docs', 'graphql',
    'robots.txt', 'sitemap.xml', 'crossdomain.xml'
]

def banner():
    print(Fore.CYAN + "=" * 65)
    print(Fore.GREEN + "   RECON SHIELD v2.0 - ADVANCED RECON & HIDDEN ENDPOINT FINDER   ")
    print(Fore.CYAN + "=" * 65)

def check_security_footprint(url):
    print(Fore.YELLOW + "\n[+] [1/4] Performing Deep Security & Server Fingerprinting...")
    try:
        response = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0"})
        headers = response.headers
        
        # 1. Check Missing Security Headers
        security_headers = {
            'Strict-Transport-Security': 'Protects against MITM / SSL Striping',
            'X-Frame-Options': 'Protects against Clickjacking',
            'X-Content-Type-Options': 'Prevents MIME-sniffing',
            'Content-Security-Policy': 'Mitigates XSS and Data Injection',
            'X-XSS-Protection': 'Legacy XSS Filter',
            'Referrer-Policy': 'Controls Referrer Information Leakage',
            'Permissions-Policy': 'Restricts Browser Features (Camera, Mic, etc.)'
        }
        
        for header, info in security_headers.items():
            if header in headers:
                print(Fore.GREEN + f"  [SAFE] {header} is present.")
            else:
                print(Fore.RED + f"  [VULN/MISSING] {header} is missing! ({info})")

        # 2. Information Disclosure
        print(Fore.YELLOW + "\n  [*] Checking Server Information Leakage...")
        if 'Server' in headers:
            print(Fore.RED + f"  [LEAK] Server Header Found: {headers['Server']}")
        if 'X-Powered-By' in headers:
            print(Fore.RED + f"  [LEAK] Technology Exposed (X-Powered-By): {headers['X-Powered-By']}")

    except Exception as e:
        print(Fore.RED + f"  [-] Error checking security footprint: {e}")

def extract_all_links_and_js(url):
    print(Fore.YELLOW + "\n[+] [2/4] Extracting Visible Links & JavaScript Files...")
    try:
        response = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract href links
        links = set()
        for a in soup.find_all('a', href=True):
            full_link = urljoin(url, a['href'])
            links.add(full_link)

        print(Fore.GREEN + f"  [+] Found {len(links)} unique links on the target page.")
        for link in list(links)[:10]:
            print(Fore.WHITE + f"   -> {link}")
        if len(links) > 10:
            print(Fore.CYAN + f"   ... and {len(links) - 10} more links.")

        # Extract JS Files for Endpoints
        print(Fore.YELLOW + "\n  [*] Extracting Embedded JavaScript Files...")
        js_files = set()
        for script in soup.find_all('script', src=True):
            full_js_path = urljoin(url, script['src'])
            js_files.add(full_js_path)

        print(Fore.GREEN + f"  [+] Found {len(js_files)} JS files for endpoint analysis.")
        for js in list(js_files)[:5]:
            print(Fore.WHITE + f"   -> {js}")

    except Exception as e:
        print(Fore.RED + f"  [-] Error extracting links/JS: {e}")

def fetch_wayback_endpoints(domain):
    print(Fore.YELLOW + "\n[+] [3/4] Passive Mining for Hidden Archived URLs (Wayback Machine)...")
    clean_domain = domain.replace("https://", "").replace("http://", "").split('/')[0]
    api_url = f"http://web.archive.org/cdx/search/cdx?url=*.{clean_domain}/*&output=json&fl=original&collapse=urlkey"
    
    try:
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            urls = res.json()
            if len(urls) > 1:
                unique_urls = list(set([u[0] for u in urls[1:]]))
                print(Fore.GREEN + f"  [+] Discovered {len(unique_urls)} historical/hidden endpoints!")
                for u in unique_urls[:12]:
                    print(Fore.WHITE + f"   -> {u}")
                if len(unique_urls) > 12:
                    print(Fore.CYAN + f"   ... and {len(unique_urls) - 12} more hidden endpoints.")
            else:
                print(Fore.RED + "  [-] No archived endpoints found.")
        else:
            print(Fore.RED + "  [-] Wayback API returned non-200 response.")
    except Exception as e:
        print(Fore.RED + f"  [-] Could not fetch archived URLs: {e}")

def check_path(base_url, path):
    target = f"{base_url.rstrip('/')}/{path}"
    try:
        res = requests.get(target, timeout=4, allow_redirects=False, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code in [200, 301, 302, 403]:
            if res.status_code == 200:
                print(Fore.GREEN + f"  [EXPOSED : 200 OK]      -> {target}")
            elif res.status_code in [301, 302]:
                print(Fore.YELLOW + f"  [REDIRECT : {res.status_code}]  -> {target}")
            elif res.status_code == 403:
                print(Fore.MAGENTA + f"  [FORBIDDEN : 403]     -> {target}")
    except:
        pass

def dir_fuzzing(url):
    print(Fore.YELLOW + "\n[+] [4/4] Multi-Threaded Fuzzing for Sensitive Paths & Admin Panels...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for path in HIGH_RISK_PATHS:
            executor.submit(check_path, url, path)

def main():
    banner()
    target = input("\nEnter target URL (e.g., https://example.com): ").strip()
    if not target.startswith("http"):
        target = "https://" + target
        
    check_security_footprint(target)
    extract_all_links_and_js(target)
    fetch_wayback_endpoints(target)
    dir_fuzzing(target)

if __name__ == "__main__":
    main()

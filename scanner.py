import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import concurrent.futures
import re

init(autoreset=True)

COMMON_PATHS = [
    'admin', 'administrator', 'login', 'wp-admin', 'dashboard',
    '.env', '.git/HEAD', 'config.php', 'backup.zip', 'db.sql',
    'api/', 'v1/', 'robots.txt', 'sitemap.xml', 'test/', 'dev/'
]

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + "   ADVANCED RECON & HIDDEN ENDPOINT FINDER   ")
    print(Fore.CYAN + "=" * 50)

def check_headers(url):
    print(Fore.YELLOW + "\n[+] Analyzing Security Headers...")
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy',
            'X-XSS-Protection'
        ]
        for header in security_headers:
            if header in headers:
                print(Fore.GREEN + f" [SAFE] {header} is present.")
            else:
                print(Fore.RED + f" [VULN/MISSING] {header} is missing!")
    except Exception as e:
        print(Fore.RED + f" [-] Error checking headers: {e}")

def fetch_wayback_urls(domain):
    print(Fore.YELLOW + "\n[+] Mining Historical & Hidden URLs (Wayback Machine)...")
    clean_domain = domain.replace("https://", "").replace("http://", "").split('/')[0]
    api_url = f"http://web.archive.org/cdx/search/cdx?url=*.{clean_domain}/*&output=json&fl=original&collapse=urlkey"
    
    try:
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            urls = res.json()
            if len(urls) > 1:
                unique_urls = list(set([u[0] for u in urls[1:]]))
                print(Fore.GREEN + f" [+] Found {len(unique_urls)} historical/hidden endpoints!")
                for u in unique_urls[:15]:
                    print(Fore.WHITE + f"  -> {u}")
                if len(unique_urls) > 15:
                    print(Fore.CYAN + f"  ... and {len(unique_urls) - 15} more hidden endpoints.")
            else:
                print(Fore.RED + " [-] No hidden archived endpoints found.")
        else:
            print(Fore.RED + " [-] Wayback API non-200 response.")
    except Exception as e:
        print(Fore.RED + f" [-] Could not fetch archived URLs: {e}")

def check_path(base_url, path):
    target = f"{base_url.rstrip('/')}/{path}"
    try:
        res = requests.get(target, timeout=3, allow_redirects=False)
        if res.status_code in [200, 301, 302, 403]:
            status_color = Fore.GREEN if res.status_code == 200 else Fore.YELLOW
            print(status_color + f" [FOUND: {res.status_code}] -> {target}")
    except:
        pass

def dir_fuzzing(url):
    print(Fore.YELLOW + "\n[+] Brute-forcing Hidden Directories & Files...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for path in COMMON_PATHS:
            executor.submit(check_path, url, path)

def main():
    banner()
    target = input("\nEnter target URL (e.g., https://example.com): ").strip()
    if not target.startswith("http"):
        target = "https://" + target
        
    check_headers(target)
    fetch_wayback_urls(target)
    dir_fuzzing(target)

if __name__ == "__main__":
    main()

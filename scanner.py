import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + "=" * 40)
    print(Fore.GREEN + "   SIMPLE WEB RECON & SECURITY TOOL   ")
    print(Fore.CYAN + "=" * 40)

def check_headers(url):
    print(Fore.YELLOW + "\n[+] Checking Security Headers...")
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy'
        ]
        
        for header in security_headers:
            if header in headers:
                print(Fore.GREEN + f"[SAFE] {header} is present.")
            else:
                print(Fore.RED + f"[MISSING] {header} is missing!")
    except Exception as e:
        print(Fore.RED + f"Error checking headers: {e}")

def scrape_links(url):
    print(Fore.YELLOW + "\n[+] Extracting Links from Homepage...")
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        count = 0
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):
                print(Fore.WHITE + f" -> {href}")
                count += 1
                if count >= 5:
                    break
        print(Fore.CYAN + f"Total displayed links: {count}")
    except Exception as e:
        print(Fore.RED + f"Error fetching links: {e}")

def main():
    banner()
    target = input("\nEnter target URL (e.g., https://example.com): ")
    if not target.startswith("http"):
        target = "https://" + target
        
    check_headers(target)
    scrape_links(target)

if __name__ == "__main__":
    main()

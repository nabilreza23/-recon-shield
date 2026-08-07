# Recon Shield - Advanced Web Recon & Hidden Endpoint Finder

An advanced Python-based CLI reconnaissance tool for ethical hackers, cybersecurity specialists, and bug bounty hunters.

## Advanced Features
- **Security Header Analysis:** Identifies misconfigurations and missing security headers (`HSTS`, `CSP`, `X-Frame-Options`, etc.).
- **Passive Hidden Endpoint Mining:** Leverages Wayback Machine APIs to uncover hidden, legacy, or forgotten endpoints (`.json`, `.php`, admin routes).
- **Multi-threaded Directory Fuzzer:** Fast brute-forcing for high-risk sensitive paths (`.env`, `admin/`, `backup.zip`, `config.php`).

## Installation
```bash
git clone https://github.com/nabilreza23/-recon-shield.git
cd recon-shield
pip install -r requirements.txt
python scanner.py

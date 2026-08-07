# Recon Shield v2.0 🛡️
> Advanced Web Reconnaissance, Security Footprinting, & Hidden Endpoint Finder for Penetration Testers and Bug Bounty Hunters.

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Recon Shield** is a powerful Python CLI tool engineered to automate initial web reconnaissance. It scans for misconfigured security headers, extracts visible & embedded JavaScript endpoints, performs passive URL mining via the Wayback Machine, and conducts multi-threaded brute-forcing for high-risk admin panels and exposed sensitive files.

---

## 🔥 Key Features

- 🛡️ **Deep Security Header & Server Footprinting:** Checks for 7+ essential HTTP security headers (`HSTS`, `CSP`, `Permissions-Policy`, etc.) and flags Server/Technology disclosure leaks (`X-Powered-By`).
- 🔗 **Visible & JS Link Mining:** Extracts all external/internal HTML hyperlinks and parses embedded JavaScript file sources.
- 📜 **Passive Wayback Endpoint Discovery:** Pulls archived and forgotten endpoints (`/api/v1/`, legacy `.php` routes) using the Wayback Machine API.
- 🚀 **Multi-Threaded Path Fuzzer:** Fast parallel scanning for exposed `.env` files, `.git` repositories, backup archives (`.sql`, `.zip`), and admin login portals (`admin/`, `cpanel`, `phpmyadmin`).

---

## 🚀 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/nabilreza23/-recon-shield.git

# Navigate into the project directory
cd recon-shield

# Install required dependencies
pip install -r requirements.txt

# Run the scanner
python scanner.py

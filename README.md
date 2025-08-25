# ⚡ HexaScan  

![Python](https://img.shields.io/badge/python-3.x-blue.svg)  
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Termux-success.svg)  
![License](https://img.shields.io/badge/license-MIT-green.svg)  

HexaScan is an **advanced port scanning and service enumeration tool** with plugin support.  
It is designed for **beginners and professionals** to quickly discover open ports, running services, and potential misconfigurations on a target system.  

With features like **fast scan, deep scan, plugin system, and web dashboard**, HexaScan gives you the flexibility to run lightweight scans or full-scale assessments.  

---

## 📑 Table of Contents
- [✨ Features](#-features)
- [📥 Installation](#-installation)
- [⚡ Usage](#-usage)
  - [Normal Scan](#-normal-scan)
  - [Fast Scan](#-fast-scan)
  - [Deep Scan](#-deep-scan)
  - [Save Output to JSON](#-save-output-to-json)
  - [View Results on Web Dashboard](#-view-results-on-web-dashboard)
  - [Network Range Scan](#-network-range-scan)
  - [Plugin Based Scanning](#-plugin-based-scanning)
- [🔌 Plugins](#-plugins)
- [📂 Project Structure](#-project-structure)
- [⚠️ Disclaimer](#️-disclaimer)
- [📌 Note](#-note)

---

## ✨ Features  

- 🚀 **Fast & Advanced Port Scanning** (Normal, Fast, Deep scan modes)  
- 🔌 **Plugin System** for service enumeration:  
  - DNS Enumeration  
  - FTP Anonymous Login Check  
  - HTTP Title Grabber  
  - MySQL & MongoDB Weak Config Check  
  - RDP Availability  
  - SMB Enumeration  
  - SSL Information Extractor  
- 📊 **Dashboard (Flask-based)** for viewing scan results in browser  
- 💾 **Save results in JSON** for further analysis  
- 🌐 **Cross-platform support** (Windows, Linux, Termux/Android)  

---

## 📥 Installation  

### 🔹 Termux (Android)  

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan
pip install -r requirements.txt
```

### 🔹 Kali Linux / Parrot OS (Debian based)  

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan
pip install -r requirements.txt
```

### 🔹 Windows  

1. Install [Python 3](https://www.python.org/downloads/)  
2. Install [Git for Windows](https://git-scm.com/download/win)  
3. Open **Command Prompt / PowerShell** and run:  

```powershell
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan
pip install -r requirements.txt
```

---

## ⚡ Usage  

### 🔹 Normal Scan  
Runs a balanced scan on default ports.  
```bash
python hexascan.py target.com --mode normal
```

### 🔹 Fast Scan  
Quick scan for common ports (21, 22, 80, 443, 3389, etc.).  
```bash
python hexascan.py target.com --mode fast
```

### 🔹 Deep Scan  
Scans all ports (1–65535) with full plugin execution.  
⚠️ May take longer.  
```bash
python hexascan.py target.com --mode full
```

### 🔹 Save Output to JSON  
```bash
python hexascan.py target.com --mode deep --output json --out-file results.json
```

### 🔹 View Results on Web Dashboard  
```bash
python dashboard.py
```
Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 🔹 Network Range Scan  
Scan entire subnet:  
```bash
python hexascan.py 192.168.1.0/24 --mode fast
```

### 🔹 Plugin Based Scanning  
Run specific checks using plugins:  
```bash
python hexascan.py target.com --plugins ftp_anon,http_title
```

---

## 🔌 Plugins  

HexaScan comes with multiple plugins to extend scanning capabilities:  

| Plugin       | Description | Example |
|--------------|-------------|---------|
| `dns_enum`   | DNS record enumeration | `python hexascan.py target.com --plugins dns_enum` |
| `ftp_anon`   | Checks anonymous FTP login | `python hexascan.py target.com --plugins ftp_anon` |
| `http_title` | Grabs HTTP page title | `python hexascan.py target.com --plugins http_title` |
| `mysql_check`| Tests MySQL weak configurations | `python hexascan.py target.com --plugins mysql_check` |
| `mongo_check`| Tests MongoDB weak configurations | `python hexascan.py target.com --plugins mongo_check` |
| `rdp_check`  | Checks RDP availability | `python hexascan.py target.com --plugins rdp_check` |
| `smb_enum`   | Enumerates SMB shares | `python hexascan.py target.com --plugins smb_enum` |
| `ssl_info`   | Extracts SSL certificate info | `python hexascan.py target.com --plugins ssl_info` |

---

## 📂 Project Structure  

```
advanced_port_scanner/
├── hexascan.py         # Main scanner script
├── dashboard.py        # Web dashboard (Flask)
├── requirements.txt    # Dependencies
├── results.json        # Example results
└── plugins/            # Service enumeration modules
```

# Installation Troubleshooting (Kali/Ubuntu PEP 668)

If you see this during `pip install` on **Kali Linux / Ubuntu (Python 3.11/3.12+)**:

```
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install python3-xyz ...
...
You can override this by passing --break-system-packages.
```

It means your system Python is **externally managed** (PEP 668). The recommended fix is to use a **virtual environment (venv)** for this project.

---

## ✅ Quick Fix (Recommended): Use a Virtual Environment

> Works on Kali, Ubuntu, Debian, Parrot, etc.

```bash
# 1) Install venv support (once)
sudo apt update
sudo apt install -y python3-venv

# 2) Go to project folder
cd HexaScan/advanced_port_scanner

# 3) Create a virtual environment ('.venv' folder)
python3 -m venv .venv

# 4) Activate the venv
source .venv/bin/activate

# 5) (optional) Upgrade pip inside venv
pip install --upgrade pip

# 6) Install project dependencies INSIDE the venv
pip install -r requirements.txt

# 7) Run HexaScan
python hexascan.py scanme.nmap.org --mode fast
# or launch dashboard
python dashboard.py

# 8) When finished, deactivate
deactivate
```

**How to know venv is active?** Your shell prompt will start with `(.venv)` and `which python` will point inside the project folder.


## 🪟 Windows (PowerShell) — Using venv

```powershell
# 1) Go to project folder
cd .\HexaScandvanced_port_scanner

# 2) Create venv
python -m venv .venv

# 3) Activate venv
.\.venv\Scripts\Activate.ps1

# 4) Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 5) Run
python hexascan.py target.com --mode normal
python dashboard.py

# 6) Deactivate
deactivate
```

If activation is blocked, run PowerShell as Admin once:
```powershell
Set-ExecutionPolicy RemoteSigned
```

---

## 📱 Termux (Android) — Using venv

```bash
pkg update && pkg upgrade -y
pkg install -y python git
git clone https://github.com/your-username/HexaScan.git
cd HexaScan/advanced_port_scanner

# Create & activate venv (no sudo in Termux)
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python hexascan.py target.com --mode fast
deactivate
```

## ❗ Common Issues & Fixes

- **`pip: command not found`** → Use `python -m pip ...` or install pip: `sudo apt install -y python3-pip` (Linux).  
- **`SSL: CERTIFICATE_VERIFY_FAILED`** → Update certs: `sudo apt install -y ca-certificates` and retry.  
- **Permission errors** → You are likely outside venv. Activate venv or avoid `sudo pip`.  
- **Still seeing PEP 668 message** → You’re not in venv. Ensure your prompt shows `(.venv)` before installing.  
- **Zsh/Fish shells** → Activation command may differ: `source .venv/bin/activate` usually works; for Fish: `source .venv/bin/activate.fish`.

---

## 📌 Why venv?

- Keeps HexaScan’s dependencies **isolated** from system Python.  
- Avoids conflicts with Kali/Ubuntu package manager (PEP 668).  
- Easy to remove: just delete the `.venv/` folder.
---

## ⚠️ Disclaimer  

HexaScan is intended for **educational and authorized security testing only**.  
Do not use this tool on systems or networks without explicit permission.  

---

## 📌 Note  

This tool was previously named **`skan`**, and has now been renamed to **HexaScan** for a better identity.  

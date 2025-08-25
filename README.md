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
git clone https://github.com/your-username/hexascan.git
cd hexascan/advanced_port_scanner
pip install -r requirements.txt
```

### 🔹 Kali Linux / Parrot OS (Debian based)  

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/your-username/hexascan.git
cd hexascan/advanced_port_scanner
pip install -r requirements.txt
```

### 🔹 Windows  

1. Install [Python 3](https://www.python.org/downloads/)  
2. Install [Git for Windows](https://git-scm.com/download/win)  
3. Open **Command Prompt / PowerShell** and run:  

```powershell
git clone https://github.com/your-username/hexascan.git
cd hexascan\advanced_port_scanner
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
python hexascan.py target.com --mode deep
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

---

## ⚠️ Disclaimer  

HexaScan is intended for **educational and authorized security testing only**.  
Do not use this tool on systems or networks without explicit permission.  

---

## 📌 Note  

This tool was previously named **`skan`**, and has now been renamed to **HexaScan** for a better identity.  

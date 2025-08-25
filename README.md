# HexaScan  

HexaScan is an **advanced port scanning and service enumeration tool** with plugin support.  
It helps you identify open ports, running services, and common misconfigurations on target machines.  
With its modular plugin system, HexaScan can easily be extended to perform custom checks.  

---

## ✨ Features  

- 🚀 **Fast & Advanced Port Scanning** (supports multiple scan modes)  
- 🔌 **Plugin System** for service enumeration:  
  - DNS Enumeration  
  - FTP Anonymous Login Check  
  - HTTP Title Grabber  
  - MySQL & MongoDB Weak Config Check  
  - RDP Availability  
  - SMB Enumeration  
  - SSL Information Extractor  
- 📊 **Dashboard (Flask-based)** for viewing scan results  
- 💾 Export results to **JSON** for further analysis  

---

## 📥 Installation  

### 🔹 Termux (Android)  

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan/advanced_port_scanner
pip install -r requirements.txt
```

### 🔹 Kali Linux / Parrot OS (Debian based)  

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan/advanced_port_scanner
pip install -r requirements.txt
```

### 🔹 Windows  

1. Install [Python 3](https://www.python.org/downloads/)  
2. Install **Git for Windows**  
3. Open **Command Prompt / PowerShell**:  

```powershell
git clone https://github.com/Prasadsarkate/HexaScan
cd hexascan\advanced_port_scanner
pip install -r requirements.txt
```

---

## ⚡ Usage  

### 🔹 Basic Scan  
```bash
python hexascan.py scanme.nmap.org --mode fast
```

### 🔹 Save Output as JSON  
```bash
python hexascan.py 192.168.1.10 --scan syn --mode fast --output json --out-file results.json
```

### 🔹 Plugin System  
Run with plugins enabled (default behavior):  

```bash
python hexascan.py target.com --mode full
```

Available plugins:  
- dns_enum  
- ftp_anon  
- http_title  
- mysql_check  
- mongo_check  
- rdp_check  
- smb_enum  
- ssl_info  

Example:  
```bash
python hexascan.py target.com --plugins ftp_anon,http_title
```

### 🔹 Run Dashboard  
To view results interactively:  

```bash
python dashboard.py
```

Now open browser at: `http://127.0.0.1:5000`

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

## 📝 Examples  

- Fast TCP Scan  
  ```bash
  python hexascan.py scanme.nmap.org --mode fast
  ```  

- SYN Scan on Internal Network  
  ```bash
  sudo python hexascan.py 192.168.1.0/24 --scan syn
  ```  

- Full Service Enumeration with JSON Output  
  ```bash
  python hexascan.py example.com --mode full --output json --out-file results.json
  ```  

---

## ⚠️ Disclaimer  

This tool is built for **educational and security testing purposes only**.  
Do not use HexaScan on networks or systems without proper authorization.  

---

## 📌 Note  

This tool was previously named **`skan`**, and has now been renamed to **HexaScan** for a better identity.  

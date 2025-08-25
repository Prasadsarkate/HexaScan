#!/usr/bin/env python3
"""
Skan - CLI scanner with plugin support.
Usage examples:
  python3 skan.py scanme.nmap.org --mode fast --output json --out-file results.json
  sudo python3 skan.py 192.168.1.10 --scan syn --mode fast
"""
from __future__ import annotations
import argparse
import socket
import ipaddress
import importlib.util
import os
import json
import time
import csv
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple

# third-party
try:
    from colorama import Fore, Style, init as colorama_init
    from prettytable import PrettyTable
except Exception:
    print("Install dependencies: pip3 install colorama prettytable")
    sys.exit(1)

# scapy optional
try:
    from scapy.all import IP, TCP, sr1, ICMP, conf as scapy_conf
    SCAPY = True
except Exception:
    SCAPY = False

colorama_init(autoreset=True)

PLUGIN_DIR = "plugins"
RESULTS_FILE_DEFAULT = "results.json"

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP", 445: "SMB"
}

TOP_100 = [80,443,22,21,25,23,53,110,445,139,3389,8080,3306,143,993,995,1723,5900,1025,587,8443,123,161,69]

# ---------- utilities ----------
def expand_targets(items: List[str]) -> List[str]:
    out = []
    for it in items:
        it = it.strip()
        if not it:
            continue
        if "/" in it:
            try:
                net = ipaddress.ip_network(it, strict=False)
                out.extend([str(ip) for ip in net.hosts()])
                continue
            except Exception:
                pass
        out.append(it)
    return out

def resolve_host(label: str) -> Tuple[str, str]:
    try:
        ip = socket.gethostbyname(label)
        return label, ip
    except Exception:
        return label, "<unresolved>"

def load_plugins() -> List[object]:
    plugins = []
    if not os.path.isdir(PLUGIN_DIR):
        return plugins
    for fname in os.listdir(PLUGIN_DIR):
        if not fname.endswith(".py"):
            continue
        if fname == "__init__.py":
            continue
        path = os.path.join(PLUGIN_DIR, fname)
        name = fname[:-3]
        try:
            spec = importlib.util.spec_from_file_location(f"{PLUGIN_DIR}.{name}", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore
            if hasattr(mod, "run"):
                plugins.append(mod)
        except Exception as e:
            print(Fore.YELLOW + f"[!] Failed to load plugin {name}: {e}")
    return plugins

# ---------- banner grabbing / probes ----------
def grab_banner_tcp(ip: str, port: int, timeout: float = 1.0) -> str:
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        # try initial recv
        try:
            data = s.recv(4096)
            if data:
                return data.decode(errors="ignore").strip()
        except Exception:
            pass
        # HTTP HEAD nudge
        try:
            if port in (80,8080,8000,8888,8443):
                s.sendall(b"HEAD / HTTP/1.0\r\nHost: %b\r\n\r\n" % ip.encode())
                resp = s.recv(4096)
                if resp:
                    return resp.decode(errors="ignore").splitlines()[0]
        except Exception:
            pass
        return ""
    except Exception:
        return ""
    finally:
        if s:
            try:
                s.close()
            except:
                pass

def tcp_connect_scan(ip: str, port: int, timeout: float = 1.0) -> Optional[Dict]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        # connect_ex returns 0 on success
        rc = sock.connect_ex((ip, port))
        if rc == 0:
            banner = grab_banner_tcp(ip, port, timeout)
            return {"ip": ip, "port": port, "proto": "tcp", "banner": banner or "", "status": "open"}
        return None
    except Exception:
        return None
    finally:
        try:
            sock.close()
        except:
            pass

def udp_probe(ip: str, port: int, timeout: float = 1.0) -> Optional[Dict]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        if port == 53:
            # small DNS query
            query = bytes.fromhex("12340100000100000000000000")
            s.sendto(query, (ip, 53))
            data, _ = s.recvfrom(1024)
            if data:
                return {"ip": ip, "port": port, "proto": "udp", "banner": "DNS response", "status": "open"}
        else:
            s.sendto(b"\x00", (ip, port))
            data, _ = s.recvfrom(1024)
            if data:
                return {"ip": ip, "port": port, "proto": "udp", "banner": "data", "status": "open"}
    except Exception:
        return None
    finally:
        try:
            s.close()
        except:
            pass
    return None

def syn_scan(ip: str, port: int, timeout: float = 1.0) -> Optional[Dict]:
    if not SCAPY:
        return None
    try:
        scapy_conf.verb = 0
        pkt = IP(dst=ip)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=timeout)
        if resp and resp.haslayer(TCP):
            flags = resp.getlayer(TCP).flags
            if flags & 0x12 == 0x12:
                return {"ip": ip, "port": port, "proto": "tcp-syn", "banner": "", "status": "open"}
    except Exception:
        return None
    return None

def ttl_os_guess(ip: str, timeout: float = 1.0) -> str:
    if not SCAPY:
        return ""
    try:
        scapy_conf.verb = 0
        pkt = IP(dst=ip)/ICMP()
        resp = sr1(pkt, timeout=timeout)
        if not resp:
            return ""
        ttl = int(resp.ttl)
        if ttl <= 64:
            return "Linux/Unix (probable)"
        if ttl <= 128:
            return "Windows (probable)"
        return "Network device (probable)"
    except Exception:
        return ""

# ---------- driver ----------
def scan_ports(ip: str, ports: List[int], scan_type: str, timeout: float, workers: int, rate: float) -> List[Dict]:
    results = []
    plugins = load_plugins()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {}
        for p in ports:
            if scan_type == "tcp":
                fut = ex.submit(tcp_connect_scan, ip, p, timeout)
            elif scan_type == "udp":
                fut = ex.submit(udp_probe, ip, p, timeout)
            elif scan_type == "syn":
                fut = ex.submit(syn_scan, ip, p, timeout)
            else:
                continue
            futures[fut] = p
            if rate and rate > 0:
                time.sleep(1.0 / rate)
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res.get("status") == "open":
                    # run plugins on this open port
                    res["plugins"] = []
                    for plugin in plugins:
                        try:
                            out = plugin.run(res["ip"], res["port"], res.get("banner", ""))
                            if out:
                                res["plugins"].append(out)
                        except Exception as e:
                            res["plugins"].append({"plugin": getattr(plugin, "__name__", "unknown"), "error": str(e)})
                    results.append(res)
                    print(Fore.GREEN + f"[+] {res['ip']}:{res['port']}/{res['proto']} OPEN | banner len={len(res.get('banner',''))} | plugins={len(res['plugins'])}")
            except Exception:
                pass
    return results

# ---------- output helpers ----------
def print_table(rows: List[Dict]):
    if not rows:
        print(Fore.YELLOW + "No open ports found.")
        return
    table = PrettyTable([Fore.CYAN + "IP", Fore.CYAN + "Port", Fore.CYAN + "Proto", Fore.CYAN + "Banner", Fore.CYAN + "Plugins"])
    for r in sorted(rows, key=lambda x: (x["ip"], int(x["port"]))):
        banner_preview = (r.get("banner") or "")[:120].replace("\n"," ")
        plugins_preview = ", ".join([p.get("plugin", p.get("name", str(p)))[:30] for p in r.get("plugins", [])]) if r.get("plugins") else ""
        table.add_row([r["ip"], r["port"], r.get("proto",""), banner_preview, plugins_preview])
    print(table)

def save_results(all_rows: List[Dict], outfmt: Optional[str], outfile: Optional[str]):
    if not outfmt:
        return
    if not outfile:
        outfile = RESULTS_FILE_DEFAULT
    if outfmt == "json":
        with open(outfile, "w", encoding="utf-8") as f:
            json.dump(all_rows, f, indent=2)
    elif outfmt == "csv":
        with open(outfile, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["target","ip","proto","port","banner","plugins"])
            w.writeheader()
            for r in all_rows:
                w.writerow({
                    "target": r.get("target",""),
                    "ip": r.get("ip",""),
                    "proto": r.get("proto",""),
                    "port": r.get("port",""),
                    "banner": (r.get("banner","")[:200]).replace("\n"," "),
                    "plugins": ";".join([str(p.get("plugin", p.get("name", ""))) for p in r.get("plugins", [])])
                })
    elif outfmt == "html":
        # simple html
        rows_html = "\n".join(f"<tr><td>{r.get('target','')}</td><td>{r.get('ip','')}</td><td>{r.get('proto','')}</td><td>{r.get('port','')}</td><td>{(r.get('banner','')[:300]).replace('<','&lt;')}</td><td>{','.join([str(p.get('plugin',p.get('name',''))) for p in r.get('plugins',[])])}</td></tr>" for r in all_rows)
        html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Skan Results</title></head><body><h1>Skan Results</h1><table border=1><thead><tr><th>Target</th><th>IP</th><th>Proto</th><th>Port</th><th>Banner</th><th>Plugins</th></tr></thead><tbody>{rows_html}</tbody></table></body></html>"""
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(html)
    print(Fore.YELLOW + f"Report saved: {outfile}")

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="Skan - scanner with plugin support")
    p.add_argument("targets", nargs="*", help="targets (names, IPs, CIDR) - or use --targets-file")
    p.add_argument("--targets-file", help="file with targets, one per line")
    p.add_argument("--mode", choices=["fast","normal","full","custom"], default="normal")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=1024)
    p.add_argument("--scan", choices=["tcp","syn","udp"], default="tcp")
    p.add_argument("--timeout", type=float, default=1.0)
    p.add_argument("--workers", type=int, default=200)
    p.add_argument("--rate", type=float, default=0.0, help="requests per second (0=unlimited)")
    p.add_argument("--output", choices=["json","csv","html"], help="save results")
    p.add_argument("--out-file", help="output filename")
    return p.parse_args()

def main():
    args = parse_args()
    inputs = []
    if args.targets_file:
        try:
            with open(args.targets_file, "r", encoding="utf-8") as f:
                inputs.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            print(Fore.RED + f"Failed to read targets file: {e}")
            sys.exit(1)
    inputs.extend(args.targets)
    if not inputs:
        print("No targets provided. Example: skan.py scanme.nmap.org --mode fast")
        sys.exit(2)
    targets = expand_targets(inputs)
    resolved = [resolve_host(t) for t in targets]
    if args.mode == "fast":
        ports = TOP_100
    elif args.mode == "normal":
        ports = list(range(1,1025))
    elif args.mode == "full":
        ports = list(range(1,65536))
    else:
        ports = list(range(max(1,args.start), min(65535,args.end)+1))

    all_results = []
    if args.scan == "syn" and not SCAPY:
        print(Fore.YELLOW + "SYN scan requested but scapy not installed; fallback to tcp. (install scapy for SYN)")
        args.scan = "tcp"

    for label, ip in resolved:
        print(Style.BRIGHT + Fore.YELLOW + f"\nScanning target: {label} ({ip})")
        if ip == "<unresolved>":
            print(Fore.RED + "Skipping unresolved target.")
            continue
        # TTL OS guess if scapy exists
        os_guess = ""
        if SCAPY:
            try:
                os_guess = ttl_os_guess(ip, timeout=args.timeout)
            except Exception:
                os_guess = ""
        if os_guess:
            print(Fore.MAGENTA + f"OS guess: {os_guess}")
        results = scan_ports(ip, ports, args.scan, args.timeout, args.workers, args.rate)
        for r in results:
            r["target"] = label
        print_table(results)
        all_results.extend(results)

    # save if requested
    if args.output:
        outname = args.out_file if args.out_file else ( "results." + args.output)
        save_results(all_results, args.output, outname)
    else:
        # also write JSON to default results.json for dashboard
        try:
            with open(RESULTS_FILE_DEFAULT, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=2)
        except:
            pass

    print(Style.BRIGHT + Fore.GREEN + "\nScan complete.")

if __name__ == "__main__":
    main()

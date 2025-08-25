import dns.query
import dns.zone

def run(ip, port, banner):
    if port != 53:
        return None
    try:
        # Example domain for testing, change if needed
        domain = "example.com"
        z = dns.zone.from_xfr(dns.query.xfr(ip, domain, timeout=5))
        return {"plugin": "dns-enum", "output": f"Zone transfer successful: {len(z.nodes)} records"}
    except Exception:
        return None

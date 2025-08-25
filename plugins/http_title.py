# plugins/http_title.py
import requests
import re
from urllib.parse import urljoin

def run(ip, port, banner):
    # only run for HTTP-like ports
    if port not in (80, 8080, 8000, 8888, 443, 8443):
        return None
    scheme = "https" if port in (443, 8443) else "http"
    url = f"{scheme}://{ip}"
    # if non-standard port, add it
    if (scheme == "http" and port != 80) or (scheme == "https" and port != 443):
        url = f"{scheme}://{ip}:{port}"
    try:
        resp = requests.get(url, timeout=4, verify=False)
        text = resp.text
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I|re.S)
        if m:
            title = m.group(1).strip()
            return {"plugin": "http-title", "title": title}
    except Exception:
        return None
    return None

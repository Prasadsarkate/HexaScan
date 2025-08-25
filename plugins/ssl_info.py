import ssl, socket

def run(ip, port, banner):
    if port != 443:
        return None
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=ip)
        conn.settimeout(3)
        conn.connect((ip, port))
        cert = conn.getpeercert()
        conn.close()
        return {
            "plugin": "ssl-info",
            "output": f"Issuer: {cert.get('issuer')}, Expiry: {cert.get('notAfter')}"
        }
    except Exception as e:
        return {"plugin": "ssl-info", "output": f"Error: {str(e)}"}

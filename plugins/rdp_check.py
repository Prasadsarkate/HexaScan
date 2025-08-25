import socket

def run(ip, port, banner):
    if port != 3389:
        return None
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, port))
        s.send(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x01\x08\x00\x03\xea\x00\x00")
        data = s.recv(1024)
        s.close()
        if data:
            return {"plugin": "rdp-check", "output": "RDP service detected (port 3389 open)"}
        return None
    except Exception as e:
        return {"plugin": "rdp-check", "output": f"Error: {str(e)}"}

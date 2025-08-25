import socket

def run(ip, port, banner):
    if port != 27017:
        return None
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, port))
        s.send(b"\x3a\x00\x00\x00\x3a\x00\x00\x00\x00\x00\x00\x00\xd4\x07\x00\x00isMaster\x00\x01\x00\x00\x00")
        data = s.recv(1024)
        s.close()
        return {"plugin": "mongo-check", "output": "MongoDB service may allow open access"}
    except Exception:
        return None

import socket

def run(ip, port, banner):
    if port != 3306:
        return None
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, port))
        data = s.recv(1024).decode(errors="ignore")
        s.close()
        return {"plugin": "mysql-check", "output": f"MySQL service detected: {data.strip()}"}
    except Exception as e:
        return {"plugin": "mysql-check", "output": f"Error: {str(e)}"}

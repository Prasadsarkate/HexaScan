# plugins/smb_enum.py
import socket

def run(ip, port, banner):
    # simple SMB presence check (does not perform intrusive enumeration)
    if port != 445:
        return None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        rc = s.connect_ex((ip, port))
        if rc == 0:
            # optionally try to recv small banner (many SMB servers won't send)
            try:
                data = s.recv(1024)
                if data:
                    preview = data[:200].hex()
                else:
                    preview = ""
            except Exception:
                preview = ""
            s.close()
            return {"plugin": "smb-enum", "open": True, "banner_preview": preview}
    except Exception:
        pass
    return None

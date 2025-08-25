# plugins/ftp_anon.py
from ftplib import FTP, error_perm

def run(ip, port, banner):
    if port != 21:
        return None
    try:
        ftp = FTP()
        ftp.connect(host=ip, port=port, timeout=4)
        # try anonymous login
        try:
            ftp.login(user='anonymous', passwd='anonymous@domain.com')
            try:
                files = ftp.nlst()  # list directory as check (may throw)
            except Exception:
                files = []
            ftp.quit()
            return {"plugin": "ftp-anon", "anonymous": True, "list_count": len(files)}
        except error_perm:
            ftp.quit()
            return {"plugin": "ftp-anon", "anonymous": False}
    except Exception:
        return None

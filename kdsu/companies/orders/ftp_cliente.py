# orders/ftp_client.py
from ftplib import FTP_TLS, error_perm

class FTPSClient:
    def __init__(self, host, username, password):
        print('HOLA ')
        self.ftp = FTP_TLS()
        print('HOLA 2')
        self.ftp.connect(host, 22)
        print('HOLA 3')
        self.ftp.login(username, password)
        print('HOLA 4')
        self.ftp.prot_p() 
        print('HOLA 5') 

    def list_files(self, path="."):
        self.ftp.cwd(path)
        return self.ftp.nlst()

    def disconnect(self):
        self.ftp.quit()
        
        
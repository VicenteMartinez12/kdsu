import paramiko
from io import BytesIO

class SFTPClient:
    def __init__(self, host, port, username, password):
        self.transport = paramiko.Transport((host, port)) 
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def list_files(self, path='.'):
        return self.sftp.listdir(path)
    
    def upload_file(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def upload_file_bytes(self, file_bytes, remote_path):
        with BytesIO(file_bytes) as fl:
            self.sftp.putfo(fl, remote_path)

    def disconnect(self):
        self.sftp.close()
        self.transport.close()

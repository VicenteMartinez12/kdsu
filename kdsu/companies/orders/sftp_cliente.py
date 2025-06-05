import paramiko

class SFTPClient:
    def __init__(self, host, port, username, password):
        self.transport = paramiko.Transport((host, port)) 
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def list_files(self, path='.'):
        return self.sftp.listdir(path)
    
    def upload_file(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def disconnect(self):
        self.sftp.close()
        self.transport.close()

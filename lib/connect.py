import paramiko
import json
# '''This is function is to execute commands on linux host
# :return: str'''


class SSHClient:
    def __init__(self, hostname1, username1, password1):
        self.hostname = hostname1
        self.username = username1
        self.password = password1

    def exec_command(self, cmd):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(self.hostname, username=self.username, password=self.password)
        _stdin, _stdout, _stderr = client.exec_command(cmd)
        stdin_out = _stdout.read().decode()
        stderr_out = _stderr.read().decode()
        client.close()
        return stdin_out, stderr_out


def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['hostname'], data['username'], data['password']


hostname, username, password = read_json("../testcases/connect.json")
connection = SSHClient(hostname, username, password)



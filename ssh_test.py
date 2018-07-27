import paramiko
import base64

ssh = paramiko.SSHClient()


key = paramiko.RSAKey.from_private_key_file("/Users/luo024/Downloads/SSHKey.pem")
#ssh.load_system_host_keys()
#ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#ssh.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)

ssh.connect('47.106.184.170', username='root', pkey=key)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')

for line in ssh_stdout:
    print(line.strip('\n'))
ssh.close()


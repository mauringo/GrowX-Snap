import sys
import time
import select
import paramiko 
time.sleep(40)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect("192.168.41.14", username="user", password="user")
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo 'user' | sudo -S ./DemoSTMicroE_new")

while(1):
    time.sleep(2)
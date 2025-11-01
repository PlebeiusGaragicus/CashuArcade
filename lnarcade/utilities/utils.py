import subprocess

def get_ip_address():
    return subprocess.getoutput("hostname -I").split()[0]

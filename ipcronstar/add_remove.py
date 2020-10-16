# add_remove.py
import subprocess, shlex
from . import ipaddrs

def add(ipaddrs):
    '''Add IP addresses''' 
    try:
        for ip in ipaddrs:
            if ':' in ip:
                command = 'ip -6 addr add {} dev eth0'.format(ip)
            else:
                command = 'ip addr add {} dev eth0'.format(ip)
            subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print(e)
        exit()

def remove(ipaddrs):
    '''Add IP addresses''' 
    try:
        for ip in ipaddrs:
            if ':' in ip:
                command = 'ip -6 addr del {} dev eth0'.format(ip)
            else:
                command = 'ip addr del {} dev eth0'.format(ip)
            subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print(e)
        exit()
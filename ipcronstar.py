#!/usr/bin/env python3

# IP Cronstar*
# Author: Billy Thompson
#
# iproute2 and cron wrapper for statically configuring IPv4 and IPv6 addresses

import subprocess, shlex, shutl, getpass, os
from sys import argv

args = argv
user = getpass.getuser()
path = '/home/{}/.ipcronstar/'.format(user)
config = path + 'ipcronstar.lst'
ipaddrs = args[2:]
usage = '''
    Simple adding/removing IPv4 and IPv6 addresses without modifying
    interface configuration or network scripts. The iproute2 package 
    must be installed.
    
    Usage: ipcronstar.py -a [address/24] [address/64] [address/56] ...
    
    -a, -r      add or remove IP addresses
    -A, -R      permenantly add or remove IP addresses
    --restore   restore IP addresses from configuration file
    '''

def add_remove_ips(action):
    global ipaddrs
    
    try:
        for ip in ipaddrs:
            if ':' in ip:
                command = 'ip -6 addr {} {} dev eth0'.format(action, ip)
            else:
                command = 'ip addr {} {} dev eth0'.format(action, ip)
            subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print(e)
        exit()

def add_permenant():
    global path, ipaddrs, config

    try:
        os.mkdir(path, 755)
    except FileExistsError:
        pass
    
    existing_addrs = []
    if os.path.exists(config):
        with open(config, 'r') as f:
            existing_addrs = f.readlines()
    
    # write config file
    ips = [ip+'\n' for ip in ipaddrs if ip not in existing_addrs]
    with open(config_file, 'a') as f:
        f.writelines(ips)

    # prepare cron
    src = __file__
    os.chmod(src, 0o700) # secure file permissions for cron script 
    dst = path + __file__
    shutil.copy(src, dst)
    cron_entry = '@reboot         root    {} --restore\n'.format(dst)

    # write crontab
    try:
        subprocess.check_output((['crontab', '-l']), stderr=subprocess.STDOUT, shell=False)
    except subprocess.SubprocessError:
        with open('mycron', 'w') as f: 
            pass
    else:
        subprocess.call(('crontab -l > mycron'), stderr=subprocess.STDOUT, shell=True)    
    
    try:
        with open('mycron', 'r') as f:
            cron_file = f.read()
            if cron_entry not in cron_file:
                with open('mycron', 'a') as f:
                    f.write(cron_entry)
        subprocess.call(('crontab mycron'), stderr=subprocess.STDOUT, shell=True)
        os.remove('mycron')                
    except Exception as e:
        print(e)
        exit()

    add_remove_ips('add')

def remove_permenant():
    global path, ipaddrs

    try:
        with open(config, 'r') as f:
            addrs = f.readlines()
    except Exception as e:
        print(e)
        exit()

    for ip in addrs:
        if ip in ipaddrs:
            del addrs[ip]
    
    ips = [ip+'\n' for ip in addrs]
    try:
        with open(config, 'w') as f:
            f.writelines(ips)
    except Exception as e:
        print(e)
        exit()
    
    add_remove_ips('del')
    
def restore_ips():
    global config, ipaddrs

    try:
        with open(config, 'r') as f:
            ipaddrs = f.readlines()
        add_remove_ips('add')
    except Exception as e:
        print(e)
        print('error reading from /etc/.ipcronstar')
        exit()

def main():
    global args, usage
    
    opts = ('-a', '-A', '-r', '-R', '--restore')
    if len(args) < 3 or args[1] not in opts:
        print(usage)
        exit()

    if args[1] == '-a':
        add_remove_ips('add')
    elif args[1] == '-r':
        add_remove_ips('del')
    elif args[1] == '-A':
        add_permenant()
    elif args[1] == '-R':
        remove_permenant()
    else:
        restore_ips()

# main
if __name__ == '__main__':
    main()
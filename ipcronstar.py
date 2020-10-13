#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Billy Thompson <rylabs@protonmail.com>
# Date: 2020-10-05

import subprocess, shlex, shutil, getpass, os
from sys import argv

args = argv
user = getpass.getuser()
path = '/root/.ipcronstar/'
config = path + 'ipcronstar.lst'
ipaddrs = args[2:]
usage = '''
    Simple adding/removing IPv4 and IPv6 addresses without modifying
    interface configuration file or network scripts. The iproute2 package 
    must be installed.
    
    Usage: ipcronstar.py -a [address/24] [address/64] [address/56] ...
    
    -a, -r      add or remove IP addresses
    -A, -R      permenantly add or remove IP addresses
    --restore   restore IP addresses from configuration file
    '''

def add_remove_ips(action):
    '''Add or remove IP sddresses'''
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

def add_permanent():
    '''Permanently add IP addresses'''
    global path, ipaddrs, config

    try:
        os.mkdir(path, 755)
    except FileExistsError:
        pass
    
    # check for existing IPs to prevent writing duplicates
    try:
        existing_addrs = []
        if os.path.exists(config):
            with open(config, 'r') as f:
                existing_addrs = [x.strip('\n') for x in f]
    
        # write config file
        ips = [ip+'\n' for ip in ipaddrs if ip not in existing_addrs]
        with open(config, 'a') as f:
            f.writelines(ips)
    except Exception as e:
        print(e)
        exit()

    # create service
    script = __file__
    os.chmod(script, 0o700) # secure permissions 
    script_dst = path + 'ipcronstar.py'
    shutil.copy(script, script_dst)
    #with open('ipcronstar.service', 'r') as f:
    #    service = f.read()
    os.chmod('ipcronstar.service', 0o755)
    service_dst = '/etc/systemd/system/ipcronstar.service'
    shutil.copy('ipcronstar.service', service_dst)
    daemon_reload = 'systemctl daemon-reload'
    enable_service = 'systemctl enable ipcronstar'
    subprocess.Popen(shlex.split(daemon_reload), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.Popen(shlex.split(enable_service), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    add_remove_ips('add')

def remove_permanent():
    '''Permanently remove IP addresses'''
    global path, ipaddrs

    try:
        # get list of IPs in config
        with open(config, 'r') as f:
            existing_addrs = [x.strip('\n') for x in f]

        # remove specified IPs from config
        [existing_addrs.remove(ip) for ip in ipaddrs]
        ips = [ip+'\n' for ip in existing_addrs]

        # write updated config
        with open(config, 'w') as f:
            f.writelines(ips)
    except Exception as e:
        e = str(e)
        if e == "list.remove(x): x not in list":
            pass
        else:
            print(e)
        exit()
    
    add_remove_ips('del')
    
def restore_ips():
    '''Restore IP addresses from config'''
    global config, ipaddrs

    try:
        with open(config, 'r') as f:
            ipaddrs = [x.strip('\n') for x in f]
        add_remove_ips('add')
    except Exception as e:
        print(e)
        print('error reading from {}'.format(config))
        exit()

def main():
    global args, usage
    
    opts = ('-a', '-A', '-r', '-R')
    if len(args) == 2 and args[1] == '--restore':
        pass
    elif len(args) < 3 or args[1] not in opts:
        print(usage)
        exit()

    if args[1] == '-a':
        add_remove_ips('add')
    elif args[1] == '-r':
        add_remove_ips('del')
    elif args[1] == '-A':
        add_permanent()
    elif args[1] == '-R':
        remove_permanent()
    else:
        restore_ips()

# main
if __name__ == '__main__':
    main()
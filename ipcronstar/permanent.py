# permanent.py
import os, shutil, shlex, subprocess
from . import add_remove, ipaddrs, config, path

service = '''[Unit]
Description=IPCronstar Restore
After=network.target

[Service]
ExecStartPre=/bin/sh -c 'until ping -c 1 8.8.8.8; do sleep 1; done;'
ExecStart=/bin/sh -c 'ipcronstar --restore'
Restart=on-failure

[Install]
WantedBy=multi-user.target
'''

def add():
    '''Permanently add IP addresses'''
    # make config file
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
    try:
        with open('ipcronstar.service', 'w') as f:
            f.write(service)
        os.chmod('ipcronstar.service', 0o644)
        shutil.copy('ipcronstar.service', '/lib/systemd/system/ipcronstar.service')
        os.remove('ipcronstar.service')
        daemon_reload = 'systemctl daemon-reload'
        enable_service = 'systemctl enable ipcronstar.service'
        subprocess.Popen(shlex.split(daemon_reload), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.Popen(shlex.split(enable_service), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except FileExistsError:
        pass
    except Exception as e:
        print(e)

    add_remove.add(ipaddrs)

def remove():
    '''Permanently remove IP addresses'''
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
    
    add_remove.remove(ipaddrs)
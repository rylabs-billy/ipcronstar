# permanent.py
import os, shutil, shlex, subprocess
from ipcronstar import add_remove, ipaddrs, config, path

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

    add_remove.add()

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
    
    add_remove.remove()
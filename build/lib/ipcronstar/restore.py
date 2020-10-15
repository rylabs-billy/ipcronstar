# restore.py
from ipcronstar import add_remove, config

'''Restore IP addresses from config'''
try:
    with open(config, 'r') as f:
        ipaddrs = [x.strip('\n') for x in f]
    add_remove.add()
except Exception as e:
    print(e)
    print('error reading from {}'.format(config))
    exit()
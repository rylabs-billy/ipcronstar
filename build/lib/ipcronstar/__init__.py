# __init__.py
__version__ = '1.0.1'

from sys import argv
args = argv
path = '/root/.ipcronstar/'
config = path + 'ipcronstar.lst'
ipaddrs = args[2:]
usage = '''
    Simple adding/removing IPv4 and IPv6 addresses without modifying
    interface configuration file or writing network scripts. Compaatible
    of systemd distributions.
    
    Usage: ipcronstar.py -a [address/24] [address/64] [address/56] ...
    
    -a, -r      add or remove IP addresses
    -A, -R      permenantly add or remove IP addresses
    --restore   restore IP addresses from configuration file
    '''
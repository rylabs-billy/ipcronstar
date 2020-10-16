# __main__.py
#import subprocess, shlex, shutil, getpass, os
#from sys import argv

from . import args, usage, ipaddrs, add_remove, permanent, restore

def main():
    opts = ('-a', '-A', '-r', '-R')
    if len(args) == 2 and args[1] == '--restore':
        pass
    elif len(args) < 3 or args[1] not in opts:
        print(usage)
        exit()

    if args[1] == '-a':
        add_remove.add(ipaddrs)
    elif args[1] == '-r':
        add_remove.remove(ipaddrs)
    elif args[1] == '-A':
        permanent.add()
    elif args[1] == '-R':
        permanent.remove()
    else:
        restore

# main
if __name__ == '__main__':
    main()
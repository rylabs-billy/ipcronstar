# IPcronstar*

A simple method of adding/removing IPv4 and IPv6 addresses without modifying interface configuration file or network scripts on Linux systems. This is particulaly helpful for cloud servers that benefit from network helper functions that would otherwise have to be disabled for static IP configuration. Takes any number of IPv4 or IPv6 addresses.

Requires Python >= 3.1.

Tested on:
- Debian 10 
- Debian 9 
- Debian 8 
- Ubuntu 20.04
- Ubuntu 19.04 
- Ubuntu 18.04



Usage:
```
ipcronstar [-a|-r|-A|-R|--restore] [address/24] [address/64] [address/56] ...
    
-a, -r      add or remove IP addresses
-A, -R      permanently add or remove IP addresses (persists reboots)
--restore   restore IP addresses from configuration file

# Example:
sudo ipcronstar -a 2400:8901:e001::c0ca:1eaf/64 192.168.170.227/17 2400:8901:e001::dead:beef/64
sudo ipcronstar -A 72.14.180.202/24 2400:8901:e001:110::60/64 2400:8901:e001:110::100/128
```
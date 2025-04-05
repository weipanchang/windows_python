#!/usr/bin/env python
import subprocess
from path import Path
import time
import re
import datetime
import shutil
import sys
from datetime import date
#from selenium_stealth import stealth
import random
import os

Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()

vpn_server_names =  [line for line in open("vpn_list_1.txt", "r")]
#n =  len(vpn_server_names)
random_server_list=  random.sample(vpn_server_names, 4)

print (random_server_list)

user_pass_pairs =  [line for line in open("UserName_Password.txt", "r")]
#n =  len(vpn_server_names)
user_pass_pairs=  random.sample(user_pass_pairs, 4)
print (user_pass_pairs)


def connect_pia_vpn(region):
    try:
        # Command to connect to PIA VPN
        # command = f'"C:\Program Files\Private Internet Access\\piactl.exe" resetsettings'
        # subprocess.run(command, shell=True, check=True)
        command = f'"C:\Program Files\Private Internet Access\\piactl.exe" set region {region}'
        subprocess.run(command, shell=True, check=True)
        command = f'"C:\Program Files\Private Internet Access\\piactl.exe" connect'
        subprocess.run(command, shell=True, check=True)
        command = f'"C:\Program Files\Private Internet Access\\piactl.exe" get region'
        subprocess.run(command, shell=True, check=True)
        print(f"Connected to PIA VPN in {region}")
    #     command = f'"C:\Program Files\Private Internet Access\\piactl.exe" disconnect'
    #     subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to PIA VPN: {e}")
        
def dis_connect_pia_vpn():
    try:
        command = f'"C:\Program Files\Private Internet Access\\piactl.exe" disconnect'
        subprocess.run(command, shell=True, check=True)
        print(f"Disconnected to PIA VPN")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disconnect to PIA VPN: {e}")

# Replace 'US' with your desired region

for i in range(4):
    
    region = random_server_list[i]
    connect_pia_vpn(region)
    
    user,password = user_pass_pairs[i].split()
#    user,password = user_pass_pair
    print(user,password)
    k = i + 1
    command = f'"3-stock_batch_data_tipranks_{k}.py" -l {user} {password}'
    os.system(command)
    # command = f'"1-stock_batch_data_tipranks_{k}.py" -l {user} {password}'
    # subprocess.run(command, shell=True, check=True)
#    os.system("pause")
    
dis_connect_pia_vpn()
# 
command = f'"5-stock_batch_data_msft_mylist_1.py"'
os.system(command)
#subprocess.run(command, shell=True, check=True)

command = f'"3-stock_batch_data_yahoo_mylist_1.py"'
os.system(command)
#subprocess.run(command, shell=True, check=True)

    
    
    
    
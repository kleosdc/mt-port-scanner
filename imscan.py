#!/usr/bin/python
# 
# Filename:  imscan.py
#
# Version: 1.0.0
#
# Author:  (imo)
#
#

import os
import clipboard
import socket, threading
from datetime import datetime

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Simple ip checker, checks if an ip address meets the qualifications of an ip address
def simple_ip_tester(ip):
    # Splitting the ip into blocks
    test_ip = ip.split('.')
    # Setting a confidence level
    confidence_level = 0
    # Checking first qualification, an ipv4 address will always be 4 blocks
    if len(test_ip) == 4:
        # for each block, check to see if block integer is less than or equal to 255
        # if so, add point to confidence level
        # else just return False because block integer is greater than 255
        #
        # Also if i is not an integer, we raise an ValueError and we let the user know that the
        # IP Address was not a qualifying IP Address
        for i in test_ip:
            try:
                if int(i) <= 255:
                    confidence_level+=1
                else:
                    return False
            except ValueError:
                print('IP Address entered does not match the qualifications of an actual IP Address.')
    # If ipv4 address is not 4 blocks then returning False
    else:
        return False

    # If confidence level is 4, return True
    if confidence_level == 4:
        return True

# Clear terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# HEADER
print(
f"""
=================================================================================
{Fore.GREEN}*{Style.RESET_ALL}           {Fore.BLUE}*{Style.RESET_ALL}            {Fore.RED}*{Style.RESET_ALL}             {Fore.RED}*{Style.RESET_ALL}{Fore.GREEN}*{Style.RESET_ALL}                {Fore.GREEN}*{Style.RESET_ALL}           {Fore.RED}*{Style.RESET_ALL}          {Fore.BLUE}*{Style.RESET_ALL}      
                    Multi Thread Port Scanner - by {Fore.MAGENTA}imo{Style.RESET_ALL} - v1.0.0
   {Fore.RED}*{Style.RESET_ALL}      {Fore.BLUE}*{Style.RESET_ALL}            {Fore.GREEN}*{Style.RESET_ALL}             {Fore.GREEN}*{Style.RESET_ALL}{Fore.BLUE}*{Style.RESET_ALL}            {Fore.BLUE}*{Style.RESET_ALL}     {Fore.GREEN}*{Style.RESET_ALL}      {Fore.RED}*{Style.RESET_ALL}         {Fore.GREEN}*{Style.RESET_ALL}{Fore.BLUE}*{Style.RESET_ALL}    {Fore.GREEN}*{Style.RESET_ALL}       
=================================================================================
"""
    )

# Get current clipboard text
clipped       = clipboard.paste()
# Checking to see if there is something
if simple_ip_tester(clipped):
    # Getting the maximum length of an ip address, Ex.: 255.255.255.255 <-- 15 Characters
    a = clipped[:15]
    # Asking whether the users wants to override the current IP Address from clipboard
    over_ride = input(f'Scanning {a}, override? y/N: ')
    # If so, user can input a new IP Address
    if over_ride.lower() == 'y':
        clipped = input('Scan Address: ')
else:
    is_valid = False
    while is_valid == False:
        clipped = input('Scan Address: ')
        if simple_ip_tester(clipped):
            is_valid = True

# Getting and Setting basic information
host          = clipped #input("Scan Address: ")
ip            = socket.gethostbyname(host)
threads       = []
open_ports    = {}
display_ports = []

def try_port(ip, port, delay, open_ports):

    sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(delay)
    result  = sock.connect_ex((ip, port))

    if result == 0:
        open_ports[port] = 'open'
        return True
    else:
        open_ports[port] = 'closed'
        return None

def scan_ports(ip, delay):
    for port in range(0, 1023):
        thread = threading.Thread(target=try_port, args=(ip, port, delay, open_ports))
        threads.append(thread)

    for i in range(0, 1023):
        threads[i].start()

    for i in range(0, 1023):
        threads[i].join()

    for i in range (0, 1023):
        if open_ports[i] == 'open':
            print(f'\nPort {str(i)} is {Back.GREEN}OPEN')
            display_ports.append(i)
        if i == 1022:
            print('\nScan Complete!')

if __name__ == '__main__':
    # Time scanner initiated
    t_start = datetime.now()

    # Start scan
    scan_ports(ip, 3)

    # Time scanner ended
    t_end   = datetime.now()

    # Check how long it took for the scan to complete
    t_total   =  t_end - t_start

    # Aligning ports in a nice order
    DR_PORTS = ','.join(map(str,display_ports))

    if DR_PORTS:
        # Displaying ports and letting the user know that the ports has been added to the clipboard
        print(f'{DR_PORTS} {Fore.YELLOW}(Copied to clipboard){Style.RESET_ALL}')

        # Adding ports to clipboard
        clipboard.copy(DR_PORTS)
    else:
        print(f'{Fore.BLUE}{Style.BRIGHT}All ports closed! (1024 scanned){Style.RESET_ALL}')

    # Displaing time elapse from start to end of script
    print(f'\nTotal time elapse: {t_total}')
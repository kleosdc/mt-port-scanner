#!/usr/bin/python
# 
# Filename:  imscan.py
#
# Latest Update: 12/29/2020
# Version: 1.0.1
#
# Author:  (imo)
#
#

import os
import sys
import clipboard
import socket, threading
from datetime import datetime

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

LATEST_VERSION = '1.0.1'

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
                return False
    # If ipv4 address is not 4 blocks then returning False
    else:
        return False

    # If confidence level is 4, return True
    if confidence_level == 4:
        return True

# Parse the user input arguments
def parse_argvs_given(arr):
    parsed_data = []
    for ar in arr:
        if ar[:2] == '-y':
            parsed_data.append(True)
        elif ar[:2] == '-P':
            try:
                ar = int(ar[2:])
                if ar <= 65535:
                    parsed_data.append(ar)
                else:
                    print(f'[{Back.RED}-{Style.RESET_ALL}] Port number provided ({ar}) exceeds the limit of 65535.')
                    parsed_data.append(1024)
            except ValueError:
                print(f'[{Back.RED}-{Style.RESET_ALL}] Port number provided is not an integer. Set to default 1024')
                parsed_data.append(1024)
        elif ar[:2] == '-h':
            print(
                """
python imscan.py
                 -h          , Shows help options menu.
                 -P65535     , Specficies the range of ports to scan. (1-65535)
                 -y          , Tell the script to skip the ip address input
                """
                )
        else:
            print(f'Unrecognized argument given: {Fore.RED}{ar}{Style.RESET_ALL}')
    return parsed_data

# Clear terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# HEADER
print(
f"""
=================================================================================
{Fore.GREEN}*{Style.RESET_ALL}           {Fore.BLUE}*{Style.RESET_ALL}            {Fore.RED}*{Style.RESET_ALL}             {Fore.RED}*{Style.RESET_ALL}{Fore.GREEN}*{Style.RESET_ALL}                {Fore.GREEN}*{Style.RESET_ALL}           {Fore.RED}*{Style.RESET_ALL}          {Fore.BLUE}*{Style.RESET_ALL}      
                    Multi Thread Port Scanner - by {Fore.MAGENTA}imo{Style.RESET_ALL} - v{LATEST_VERSION}
   {Fore.RED}*{Style.RESET_ALL}      {Fore.BLUE}*{Style.RESET_ALL}            {Fore.GREEN}*{Style.RESET_ALL}             {Fore.GREEN}*{Style.RESET_ALL}{Fore.BLUE}*{Style.RESET_ALL}            {Fore.BLUE}*{Style.RESET_ALL}     {Fore.GREEN}*{Style.RESET_ALL}      {Fore.RED}*{Style.RESET_ALL}         {Fore.GREEN}*{Style.RESET_ALL}{Fore.BLUE}*{Style.RESET_ALL}    {Fore.GREEN}*{Style.RESET_ALL}       
=================================================================================
"""
    )

# Get current clipboard text
clipped       = clipboard.paste()[:15]

# Get arguments passed in
parse_argv = sys.argv[1::]

# Default settings
SELECTED_PORTS = 1024
SKIP_FORWARD = False

# Print script command
print('python' ,' '.join(map(str,sys.argv)), '\n')

for arg in parse_argvs_given(parse_argv):
    if type(arg) == bool:
        SKIP_FORWARD = arg
    elif type(arg) == int:
        SELECTED_PORTS = arg

if SELECTED_PORTS == 1024:
    print(f'[{Back.RED}-{Style.RESET_ALL}] Port Range. [DEFAULT TO 1-{SELECTED_PORTS}]')
else:
    print(f'[{Back.GREEN}+{Style.RESET_ALL}] Port Range. [1-{SELECTED_PORTS}]')

if SKIP_FORWARD == False:
    print(f'[{Back.RED}-{Style.RESET_ALL}] Skipped.')
else:
    if not simple_ip_tester(clipped):
        print(f'IP obtained from your clipboard did not meet the IP Address format. ({Fore.RED}{clipped}{Style.RESET_ALL})')
    else:
        print(f'[{Back.GREEN}+{Style.RESET_ALL}] Skipped.')


# Checking to see if there is something
if simple_ip_tester(clipped):
    # Getting the maximum length of an ip address, Ex.: 255.255.255.255 <-- 15 Characters
    a = clipped
    if not SKIP_FORWARD:
        # Asking whether the users wants to override the current IP Address from clipboard
        over_ride = input(f'Scanning {a}, override? y/N: ')
        # If so, user can input a new IP Address
        if over_ride.lower() == 'y':
            clipped = input('Scan Address: ')
    else:
        print(f'Scanning {a}...')
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

	try:
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
	except:
		pass

	

def scan_ports(ip, delay, ports_scan):
    for port in range(0, ports_scan-1):
        thread = threading.Thread(target=try_port, args=(ip, port, delay, open_ports))
        threads.append(thread)

    for i in range(0, ports_scan-1):
        threads[i].start()

    for i in range(0, ports_scan-1):
        threads[i].join()

    for i in range (0, ports_scan-1):
    	try:
    		if open_ports[i] == 'open':
    			print(f'\nPort {str(i)} is {Back.GREEN}OPEN')
    			display_ports.append(i)
    		if i == ports_scan-2:
    			print('\nScan Complete!')
    	except:
    		pass

if __name__ == '__main__':
    # Time scanner initiated
    t_start = datetime.now()

    # Start scan
    scan_ports(ip, 3, SELECTED_PORTS)

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

import subprocess

import optparse

import re

import os

import random

import pyfiglet

from termcolor import colored

def banner():

    custom_fig = pyfiglet.Figlet(font='banner')

    print(colored(custom_fig.renderText('Change my MAC!')))

    print(colored("\n***************************************************************************************************************************"))
    
    print(colored("\t\t\t\t\t\t  Author  : d4rkpr1nce\n\t\t\t\t\t\t GitHub  : https://github.com/d4rkpr1nce",'cyan',attrs=['bold']))
    
    print("***************************************************************************************************************************")    

def get_input():

    sample = "sudo python3 changemymac.py -i [interface] -[option] [argument]"

    parse_object = optparse.OptionParser(usage=sample)

    parse_object.add_option("-i","--interface",dest = "interface", help="The interface that is going to be changed its MAC address.")

    parse_object.add_option("-m","--mac", dest="mac", help="New MAC address")
    
    parse_object.add_option("-c","--current",dest="current",help="Print the current MAC address",nargs=0)
    
    parse_object.add_option("-r","--random",dest="random",help="Set fully random MAC",nargs=0)
    
    parse_object.add_option("-V","--version",dest="version",help="Print version",nargs=0)
   
    parse_object.add_option("-s","--samevendor",dest="same",help="Assign a random MAC address from your original MAC same vendor",nargs=0)
    
    parse_object.add_option("-o","--original",dest="original",help="Replaces the current MAC address with the MAC address assigned by the vendor",nargs=0)
    
    parse_object.add_option("-l","--like",dest="like",help="Set random vendor MAC of the same kind",nargs=0)
    
    parse_object.add_option("-a","--another",dest="another",help="Set random vendor MAC of the any kind",nargs=0)
    
    parse_object.add_option("-v", "--vendor", dest="vendor", help="Assign a random MAC address for the vendor you want [XX:XX:XX]",nargs=1)
    
    parse_object.add_option("-L", "--list", dest="list", help="Print known vendors",nargs=0)
    
    (user_input,arguments) = parse_object.parse_args()
    
    return user_input 

def mac_changer(interface, mac, original_mac, user_input):
    
    current_mac = check_new_mac(interface)
    
    print("[+] Trying to change the current MAC address")
    
    subprocess.call(["ifconfig", interface, "down"])
    
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    
    subprocess.call(["ifconfig", interface, "up"])

    new_mac = check_new_mac(interface)

    if str(current_mac).upper() != str(new_mac).upper() or get_input == ():

        original_vendor = vendor("/home/dkp/Masaüstü/projects/oui.txt",original_mac[0:8].upper())
        
        current_vendor = vendor("/home/dkp/Masaüstü/projects/oui.txt",current_mac[0:8].upper())

        new_vendor = vendor("/home/dkp/Masaüstü/projects/oui.txt",new_mac[0:8].upper())

        vendors = [original_vendor, current_vendor, new_vendor]

        for i in vendors:

            if i == "":
                
                i = "Unknown\n"

        print(f"Your MAC Address was changed from {current_mac} to {new_mac}")

        print(f"\nORIGINAL MAC : {original_mac} {original_vendor}")

        print(f"CURRENT MAC: {current_mac} {current_vendor}")
        
        print("NEW MAC      : " + new_mac + "    " + new_vendor)
    
    else:
        
        print("[!] An error occured while changing the MAC address.")

def check_new_mac(interface):
    
    ifconfig = subprocess.check_output(["ifconfig",interface])
    
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))
    
    if new_mac:
        
        return new_mac.group(0)

    else:

        return None

def oui_list(file):
    
    oui_list = []
    
    with open(file,'r') as ouifile:

        lines = ouifile.readlines()

        for line in lines:

            oui_list.append(line)

    return oui_list

def wireless_list(file):
    
    wireless_list = []
    
    with open(file,'r') as ouifile:

        lines = ouifile.readlines()

        for line in lines:

            wireless_list.append(line)

    return wireless_list

def random_mac(part_number):

    mac = []
    
    hex = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    
    for _ in range(part_number):

        mac.append(hex[random.randint(0,15)] + hex[random.randint(0,15)])
       
    return  ':'.join(mac)

def same_vendor_mac(user_interface, original_mac,user_input):

    mac = random_mac(3)
    
    new_mac = original_mac[0:9] +  mac
    
    mac_changer(user_interface, new_mac, original_mac,user_input)

def like_mac(user_interface,original_mac,user_input):

    wirelesses_list = wireless_list("wireless_card.txt")
    
    mac = random_mac(3)
    
    vendor_bytes = wirelesses_list[random.randint(0,39)]
    
    like_mac = vendor_bytes[0:2] + ":" + vendor_bytes[3:5] + ":" + vendor_bytes[6:8] + ":" + mac
    
    mac_changer(user_interface,like_mac,original_mac,user_input)

def another_vendor_mac(user_interface,original_mac,file_name,user_input):
    
    vendor = original_mac[0:8]
    
    oui = oui_list(file_name)
    
    mac = random_mac(3)
    
    index = 0

    for i in oui:
        
        if i.find(vendor) == -1:
            
            index = index + 1
        
        else:
            
            oui.pop(index)
            
            break
    
    new_mac = oui[random.randint(0,len(oui)-1)][0:8] + ":" + mac
    
    mac_changer(user_interface,new_mac,original_mac,user_input)

def set_mac(user_interface,mac,original_mac,user_input):
    
    mac_changer(user_interface,mac,original_mac,user_input)


def user_choice_vendor(user_vendor,user_interface,original_mac,user_input):
    
    mac = random_mac(3)
    
    new_mac = user_vendor + ":" + mac
    
    mac_changer(user_interface, new_mac, original_mac,user_input)

def list_vendors(file_name):

    with open(file_name, 'r') as filename:
        
        for line in filename:

            print(line)


def vendor(file_name,vendor_bytes):
    
    index = 0
    
    vendor = ""
    
    with open(file_name, 'r') as filename:
      
        for i in filename:

            if i.find(vendor_bytes) != -1:
            
                vendor = i[14:len(i)]
            
            break
    
    return vendor

def reset_mac(interface):
        
    ethtool = subprocess.check_output(["ethtool", "-P", interface])
    
    permanent_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ethtool))
    
    if permanent_mac:
    
        return permanent_mac.group(0)
    
    else:
    
        return None

def validate_mac(mac):
    
    return re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower())

def main():

    banner()

    user_input = get_input()

    if user_input.interface:

        try:
    
            original_mac = reset_mac(user_input.interface)

            if user_input.current == () :

                print("Your current MAC Address is: " + check_new_mac(user_input.interface))

            elif user_input.mac and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.same == None and user_input.vendor == None:
                
                if validate_mac(user_input.mac):
                    
                    mac_changer(user_input.interface, user_input.mac,original_mac,user_input.original)
                        
                else:
                        
                    print('[-] MAC Address you entered is not valid.')

            elif user_input.random == () and user_input.original == None and user_input.like == None and user_input.another == None and user_input.same == None and user_input.mac == None and user_input.vendor == None:

                new_mac = random_mac(6)

                mac_changer(user_input.interface, new_mac, original_mac, user_input.original)
            
            elif user_input.same == () and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:

                same_vendor_mac(user_input.interface, original_mac, user_input.original)

            elif user_input.original == () and user_input.same == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:
                
                mac_changer(user_input.interface, original_mac, original_mac, user_input.original)
                
            elif user_input.like == () and user_input.original == None and user_input.same == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:

                like_mac(user_input.interface, original_mac, user_input.original)

            elif user_input.another == () and user_input.original == None and user_input.like == None and user_input.same == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:

                another_vendor_mac(user_input.interface, original_mac, "/home/dkp/Masaüstü/projects/oui.txt", user_input.original)
                
            elif user_input.vendor and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.same == None:

                user_choice_vendor(user_input.vendor, user_input.interface, original_mac, user_input.original)
            
            else:

                print("[!] Please select only one of the parameters after you specify the interface. For options try -h parameter.")

        except FileNotFoundError:

            print("[!] You are missing one of your files.")
        
        except:

            print("[!] Please install ethtool to Change your MAC.")
        
            original_mac = check_new_mac(user_input.interface)
            
    elif user_input.version == ():
        
        print("Version 3.0")

    elif user_input.list == ():
   
        list_vendors("oui.txt")

    else:
   
        print("[!]Please check out the usage with -h.")

if __name__ == '__main__':
    
    main()

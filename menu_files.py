from main import *
from scapy.all import*
from attacks import *
import os
import time

menudict = {
    "mod_attack_IP": "Modify attacker IP address",
    "mod_target_IP": "Modify target IP address",
    "mod_target_port": "Modify target port number",
    "SYN_flood": "SYN flood attack",
    "ACK_flood": "ACK flood attack",
    "lpacket": "Long packet attack",
    "httphackery": "Malformed HTTP request",
    "udpteardrop": "Fragmented UDP packet with malformed offset",
    "TCPteardrop": "Fragmented TCP packet with malformed offset",
    "ARPSpoof": "ARP spoofing for MIM",
    "telnet_long": "Telnet long string attack",
}

def printsplash():
    print("""
    +---------------------------------------------------------------------------+
    |   __________                           __________             .__         |
    |   \____    /___________  ____          \______   \__ __  _____|  |__      |
    |     /     // __ \_  __ \/ ___\   ______ |       _/  |  \/  ___/  |  \     |
    |    /     /\  ___/|  | \/ /_/  > /_____/ |    |   \  |  /\___ \|   Y  \    |
    |   /_______ \___  >__|  \___  /          |____|_  /____//____  >___|  /    |
    |           \/   \/     /_____/                  \/           \/     \/     |
    +---------------------------------------------------------------------------+
    |           Welcome to Zerg rush, a simple network attacking tool.          |
    +---------------------------------------------------------------------------+
    |                                                       Peter Lee, UIUC 2022|
    |                                                      wonjong3@illinois.edu|
    |                                                 peterwlee.web.illinois.edu|
    |                                                      Github.com/wonjongbot|
    +---------------------------------------------------------------------------+
    """)

def printInfo(src, dst, dport):
    # if destination port is normal, promopt normal info
    if (dport != -1):
        print("[*] Attack information:\n    Attacker IP: "+src+"\n    Target IP: "+dst+"\n    Target port number: "+str(dport)+"\n")
    else:
        print("[*] Attack information:\n    Attacker IP: "+src+"\n    Target IP: "+dst+"\n    Target port number: NULL\n")
    
    # cases for when user argument does not exist
    if (src == "NULL"):
        print("[!] Attacker IP address is NULL. Please use opiton 3 to enter argument.")
    if (dst == "NULL"):
        print("[!] Target IP address is NULL. Please use opiton 3 to enter argument.")
    if (dport == int("-1")):
        print("[!] Target port is NULL. Please use opiton 3 to enter argument.\n")

def printOption():
    print("[*] Please select options below:")
    i = 1
    for k in menudict.items():
        print("    "+str(i)+". "+k[1])
        i+=1

def menulogic(src, dst, dport):
    foo = input("\nzRush > ")
    print("\n[*] You have selected "+ foo)
    if foo == "1":
        tmp = src
        src = input("Enter new attacker IP address or type \"back\" below\n\nzRush > ")
        if (src == "back"):
            selection(tmp, dst, dport)
        else:
            selection(src, dst, dport)
    elif foo == "2":
        tmp = dst
        dst = input("Enter new target IP address or type \"back\" below\n\nzRush > ")
        if (dst == "back"):
            selection(src, tmp, dport)
        else:
            selection(src, dst, dport)
    elif foo == "3":
        tmp = dport
        dport = input("Enter new target port number or type \"back\" below\n\nzRush > ")
        if (dport == "back"):
            selection(src, dst, tmp)
        else:
            selection(src, dst, dport)
    elif foo == "4":
        syn_flood(src, dst, dport)
    elif foo == "5":
        ACK_attack(src, dst, dport)
    elif foo == "6":
        lpacket_raw(src,dst, dport)
    elif foo == "7":
        HTTPhackery(src,dst, dport)
    elif foo == "8":
        UDPteardrop(src, dst, dport)
    elif foo == "9":
        TCPteardrop(src, dst, dport)
    elif foo == "10":
        ARPSpoof(src, dst, dport)
    elif foo == "11":
        telnet_long(src, dst, dport)
        print("hello")
    else:
        selection(src, dst, dport)
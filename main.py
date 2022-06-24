from menu_files import *

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
    else:
        selection(src, dst, dport)

def selection(src, dst, dport):
    os.system("clear -x")
    # print splash screen
    printsplash()

    # print attack info
    printInfo(src, dst, dport)

    printOption()

    menulogic(src, dst, dport)

if __name__ == "__main__":
    from scapy.all import*
    from attacks import *
    import os

    try:
        src = sys.argv[1]
        dst = sys.argv[2]
        dport = int(sys.argv[3])
    except:
        src = "NULL"
        dst = "NULL"
        dport = int("-1")
    try:
        selection(src, dst, dport)
    except KeyboardInterrupt:
        print("\n[!] exiting Zerg Rush. See ya!")

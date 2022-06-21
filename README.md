# Zerg-Rush

Zerg-Rush is a pentesting tool for Denial of Service (DoS) attacks in TCP networks, primarily to test vulnerabilties of industrial control systems (ICS). 

## Installation / dependencies

This project is heavily based on scapy python library. Please install scapy with following command:

> pip install --pre scapy[basic]

## Usage

The program requires root privelidge to send packets.

Run the program by executing main.py.

main.py takes three arguments, where respectively be used as attacker ip address, target ip address, and target port:

> python3 main.py [attacker IP] [target IP] [target port]

example:
> python3 main.py 192.168.0.1 192.168.0.2 5555

no commandline arguments sets all three values as NULL, which must be changed in the menu.

## Menu Navigation

Zerg Rush offers CLI menu navigation to select types of attack and modify attack configurations. A menu screen would look something like below:

``` console
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
                                                            Peter Lee, UIUC 2022
[*] Attack information:
    Attacker IP: 192.168.0.1
    Target IP: 192.168.0.2
    Target port number: 5555

[*] Please select options below:
    1. SYN flood attack
    2. ACK flood attack
    3. Modify attacker IP address
    4. Modify target IP address
    5. Modify target port number
zRush >
```

## Attacks

When TCP/IP connection is initilaized, 3-way handshake is performed between the server and the client. 

### SYN flood attack

In SYN flood mode, the attacker sends spoofed, raw SYN packets to the target indefinitely. The target will respond by sending SYN/ACK packet, which the attacker will disregard. Therefore, the target computer will initiate half-open connections until its resource is depleted. 

### ACK flood attack

In ACK flood mode, the attacker establishes a full connection to the target by sending ACK packet after receiving SYN/ACK from the target. The attacker continues this indefinitely, which prevents the target from serving legitimate users. To perform ACK flood attack, the attacker's kernal must disregard SYN/ACK packet received as kernal will respond with RST to the connections it did not initiate (main.py did!). Therefore attacker's machine must filter out / drop any outgoing RST packets. Such setting can be configured using iptables.

> sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

However, Zerg-Rush already runs this command whenever ACK flood attack is initiated. Also, the filtering above is reverted once the user exits the program.

### Long string flooding

Sends very long string to designated IP and PORT

### HTTP malformed request

Sends malformed req through HTTP

### Teardrop(UDP)

Sends fragmented UDP with malformed offset

## Achievements

Here are some notes from experiements performed with Zerg-rush

### ABB REF615 Feeder Protection and Control Relay

#### HTTP server

_SYN flood attack_:

- Target port: 80
- Affect: HTTP server crashed

_ACK flood attack_:

- Target port: 80
- Affect: HTTP server crashed

_long string attack_:

- Target port: 80
- Affect: when attack runs, program crashes after returning broken pipe error, indicating that the server cut the connection off. No noticeable affect on WHMI page of the relay. Wireshark shows that the relay sends RST to the attacker.

_malformed HTTP request_:

- Target port: 80
- experiment: very long request form
  - Normal HTTP request structure:
  > GET [PATH] HTTP/1.1\r\nHost: [HOST]\r\n\r\n
  - Test 1 - long string:
    - Sending very long, no carriage return character
      - request sent:
        > GET [PATH]XXXXXXXXX[...]XXXXXXXXX HTTP/1.1\r\nHost: [HOST]\r\n\r\n
      - effect: 400 error
      - server response:
        > b'E\x00\x00j\x01\xb6\x00\x00@\x06\xf5g\xc0\xa8\x01\x0f\xc0\xa8\x01\x11\x00P\xf2\xf5\xe8\xd3YG\x00\x00\x04>P\x18\x12{5\xe3\x00\x00HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'

    - Test 2 - relative path:
      - Sending a malformed request that has relative path to traverse into parent folders
      - request sent:
        > "GET [PATH]/../../ HTTP/1.1\r\nHost: [HOST]\r\n\r\n"
      - effect: 404 error
      - server response:
        > b'E\x00\x00\x8a\x01\xc5\x00\x00@\x06\xf58\xc0\xa8\x01\x0f\xc0\xa8\x01\x11\x00P@\xc3\x934\xb0\xf1\x00\x00\x00EP\x18\x16t\xc4\x1a\x00\x00HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nTransfer-Encoding: chunked\r\nConnection: close\r\n\r\n'

### SEL-751 Feeder Protection Relay

#### FTP server

_SYN flood attack_:

- Target port: 21
- Affect: FTP server seems to be slowed down. Sometimes returns this message before correctly returning command

> 229 Entering Extended Passive Mode (|||PORT NUM|).

_ACK flood attack_:

- Target port: 21
- Affect: FTP server crashed with message like below

> 421 Service not available, remote server has closed connection.
226 Closing data connection.

_Long String Attack_

- Target port: 21
- running two processes of this attacks blocks other users from connecting through FTP because SEL only allows 2 ftp connections
- I can hear relay clicks whenever one fails to log into FTP.

## Future Goals

- Experiment with different flooding attacks and their affects on ICS's critical system
  - test connection to serial port to read out malfunctions & etc
- Modify ACK attack s.t. I don't use sr1 command (keep them seperate so whenever SYN/ACK comes in send ACK packet. No need to send wait send wait send wait..)
- Send very long packets with no carriage return
  - super long ID/PW
  - malformed HTTP request
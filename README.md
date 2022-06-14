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
```
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

### SEL-751 Feeder Protection Relay

#### FTP server

_SYN flood attack_:
- Target port: 21
- Affect: FTP server seems to be slowed down. Sometimes returns this message before correctly returning command
> 229 Entering Extended Passive Mode (|||34771|).

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
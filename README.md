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
>
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

#### SYN flood attack
Target port: 80

Affect: HTTP server crashed

#### ACK flood attack
Target port: 80

Affect: HTTP server crashed

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

## network/vulnerability scans

### REF 615

#### nmap scan

- nmap port scan

``` console
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-17 14:10 CDT
Nmap scan report for 192.168.1.15
Host is up (0.00050s latency).
Not shown: 997 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
20000/tcp open  dnp
MAC Address: 00:90:4F:E5:28:CF (ABB Power T&D Company)

Nmap done: 1 IP address (1 host up) scanned in 6.36 seconds
```

- nmap OS scan

``` console
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-17 14:16 CDT
WARNING: RST from 192.168.1.15 port 21 -- is this port really open?
WARNING: RST from 192.168.1.15 port 21 -- is this port really open?
Nmap scan report for 192.168.1.15
Host is up (0.00046s latency).
Not shown: 997 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
20000/tcp open  dnp
MAC Address: 00:90:4F:E5:28:CF (ABB Power T&D Company)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.92%E=4%D=6/17%OT=21%CT=1%CU=36613%PV=Y%DS=1%DC=D%G=Y%M=00904F%T
OS:M=62ACD31F%P=x86_64-redhat-linux-gnu)SEQ(SP=A8%GCD=1%ISR=AE%TI=I%CI=I%II
OS:=I%TS=A)OPS(O1=M5AENW0NNSNNT11%O2=M578NW0NNSNNT11%O3=M280NW0NNT11%O4=M5A
OS:ENW0NNSNNT11%O5=M218NW0NNSNNT11%O6=M109NNSNNT11)WIN(W1=1688%W2=15B0%W3=1
OS:12C%W4=1688%W5=126C%W6=11CA)ECN(R=Y%DF=N%T=40%W=16B8%O=M5AENW0NNS%CC=N%Q
OS:=)T1(R=Y%DF=N%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=N%T=40%
OS:W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=N%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=
OS:)T6(R=Y%DF=N%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=N%T=40%W=0%S=Z%A=
OS:S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=FF%IPL=38%UN=0%RIPL=G%RID=G%RIPCK=G%RUC
OS:K=G%RUD=G)IE(R=Y%DFI=N%T=FF%CD=S)

Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.91 seconds
```

- nmap vulnerabiltiy scan

``` console
foo@bar:~$ nmap -sV --script vuln 192.168.1.15
Starting Nmap 7.80 ( https://nmap.org ) at 2022-06-17 15:01 CDT
Nmap scan report for 192.168.1.15
Host is up (0.0011s latency).
Not shown: 997 closed ports
PORT      STATE SERVICE    VERSION
21/tcp    open  ftp        NET Disk/NetStore ftpd (Disabled)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
80/tcp    open  tcpwrapped
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2014-3704: ERROR: Script execution failed (use -d to debug)
20000/tcp open  dnp?
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
```

#### nikto scan

``` console
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          192.168.1.15
+ Target Hostname:    192.168.1.15
+ Target Port:        80
+ Start Time:         2022-06-17 14:01:02 (GMT-5)
---------------------------------------------------------------------------
+ Server: No banner retrieved
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: GET, HEAD, POST, PUT 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ /catinfo?<u><b>TESTING: The Interscan Viruswall catinfo script is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ /search.asp?term=<%00script>alert('Vulnerable')</script>: ASP.Net 1.1 may allow Cross Site Scripting (XSS) in error pages (only some browsers will render this). http://www.cert.org/advisories/CA-2000-02.html.
+ OSVDB-27071: /phpimageview.php?pic=javascript:alert(8754): PHP Image View 1.0 is vulnerable to Cross Site Scripting (XSS).  http://www.cert.org/advisories/CA-2000-02.html.
+ OSVDB-3931: /myphpnuke/links.php?op=search&query=[script]alert('Vulnerable);[/script]?query=: myphpnuke is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ OSVDB-3931: /myphpnuke/links.php?op=MostPopular&ratenum=[script]alert(document.cookie);[/script]&ratetype=percent: myphpnuke is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ /modules.php?op=modload&name=FAQ&file=index&myfaq=yes&id_cat=1&categories=%3Cimg%20src=javascript:alert(9456);%3E&parent_id=0: Post Nuke 0.7.2.3-Phoenix is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ /modules.php?letter=%22%3E%3Cimg%20src=javascript:alert(document.cookie);%3E&op=modload&name=Members_List&file=index: Post Nuke 0.7.2.3-Phoenix is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ OSVDB-4598: /members.asp?SF=%22;}alert(223344);function%20x(){v%20=%22: Web Wiz Forums ver. 7.01 and below is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ OSVDB-2946: /forum_members.asp?find=%22;}alert(9823);function%20x(){v%20=%22: Web Wiz Forums ver. 7.01 and below is vulnerable to Cross Site Scripting (XSS). http://www.cert.org/advisories/CA-2000-02.html.
+ 6544 items checked: 5155 error(s) and 12 item(s) reported on remote host
+ End Time:           2022-06-17 14:01:46 (GMT-5) (44 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

```

#### nmap + metasploit scan

```console
msf6 auxiliary(scanner/portscan/tcp) > run

[+] 192.168.1.15:         - 192.168.1.15:80 - TCP OPEN
[*] 192.168.1.15:         - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(scanner/portscan/tcp) > db_nmap -sV -p 80 192.168.1.15
[-] The nmap executable could not be found
msf6 auxiliary(scanner/portscan/tcp) > db_nmap -sV -p 80 192.168.1.15
[*] Nmap: Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-17 13:53 CDT
[*] Nmap: Nmap scan report for 192.168.1.15
[*] Nmap: Host is up (0.0014s latency).
[*] Nmap: PORT   STATE SERVICE    VERSION
[*] Nmap: 80/tcp open  tcpwrapped
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 6.11 seconds
msf6 auxiliary(scanner/portscan/tcp) > db_nmap -sV -A -p 80 192.168.1.15
[*] Nmap: Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-17 13:54 CDT
[*] Nmap: Nmap scan report for 192.168.1.15
[*] Nmap: Host is up (0.0010s latency).
[*] Nmap: PORT   STATE SERVICE    VERSION
[*] Nmap: 80/tcp open  tcpwrapped
[*] Nmap: |_http-title: Login
[*] Nmap: | http-methods:
[*] Nmap: |_  Potentially risky methods: PUT
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 10.54 seconds
```

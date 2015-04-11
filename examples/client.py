#connect to server, send and receive json data
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 31337
s.connect((host,port))


s.write(json.dumps({'message':'hello world!', 'test':123.4}))
data = s.read()
print "Received: " + json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

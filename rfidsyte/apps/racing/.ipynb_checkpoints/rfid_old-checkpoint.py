import socket
import time

sock = socket.socket()
print('socket defined')
sock.connect(('192.168.1.190', 6000))
print('socket connected')
sock.send(b'\x04\xff\x21\x19\x95')
ts=time.time()










while(True):
    sock.send(b'\x04\x00\x01\xdb\x4b')
    data = sock.recv(64)
    print ('received1024: ' , data," time:",time.time()-ts)
    ts=time.time()










sock.close()
print ('sock closed')
print('data received: ',data)



import socket
import threading

s= socket.socket()
s.connect(("192.168.56.1", 2234))

def msg():
      a=input()
      while a != 'bey':
            s.send(a.encode())
            a = input()
      else:
            s.close()
t = threading.Thread(target=msg)
t.start()

while True:
      try:
            print(s.recv(1024).decode())
      except:
            pass
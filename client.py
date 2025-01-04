import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 25565))

def recv():
  try:
    return json.loads(sock.recv(1024).decode())
  except:
    return False

def send(d):
  try:
    sock.send(json.dumps(d).encode())
  except:
    return False

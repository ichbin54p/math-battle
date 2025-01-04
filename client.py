import socket
import json
from sys import argv

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[0], argv[1]))

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

send({
    "op": 0,
    "d": {
        "username": input("Enter Username: ")
    }
})

while True:
    d = recv()
    
    if not d:
        print("Error recieving math equation from server")
        break
    
    if d['op'] == 1:        
        answer = input(f"Math equation: {d['d']['sum']} = ")
                
        if not send({"op": 1, "d": {"answer", answer}}):
            print("Error submitting answer")
            break

        response = recv()

        if not response:
            print("Error recieving response from server")
            break
            
        if response['op'] == 2:
            if response['d']['correct']:
                print(f"{answer} is correct!")
                break
            else:
                print(f"{answer} is incorrect")

print("Game finished!")
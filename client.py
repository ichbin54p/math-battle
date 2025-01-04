import socket
import json
from sys import argv

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[1], int(argv[2])))

if len(argv) < 2:
    exit("Usage: python3 client.py <ip> <port>")

def recv():
    d = sock.recv(1024).decode()

    try:
        return json.loads(d)
    except:
        print(f"Error decoding {d}")
        return False

def send(d):
    try:
        sock.send(json.dumps(d).encode())
        return True
    except:
        print(f"Error sending {d}")
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
                
        if not send({"op": 1, "d": {"answer": float(answer)}}):
            print("Error submitting answer")
            break

        response = recv()

        if not response:
            print("Error recieving response from server")
            break
            
        if response['op'] == 2:
            if response['d']['correct']:
                print(f"{answer} is correct!")
            else:
                print(f"{answer} is incorrect")

print("Game finished!")
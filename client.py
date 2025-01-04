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


# Send server authorization intents, op = 1

send({
    "op": 0,
    "d": {
        "username": input("Enter Username: ")
    }
})

# Communicate with server

while True:
    d = recv()
    
    if not d:
        print("Error recieving math equation from server")
        break
    
    # if op == 1 that means it's a math equation

    if d['op'] == 1:
        # Loop in the math eqation until it's correct
        
        while True:
                # Print the math equation, the server will send something like x + y
        
                answer = input(f"Math equation: {d['d']['sum']} = ")
                
                # Send the answer and await a response
        
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
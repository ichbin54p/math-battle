import socket
import json
from threading import Thread
from random import randint
from sys import argv

if len(argv) < 3:
    exit("Usage: python3 server.py <ip> <port> <max clients>")

symbols = ["+", "-", "*", "/"]

class equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.s = "+"
        self.r = self.a + self.b
    def e(self):
        return f"{self.a} {self.s} {self.b}"
    def n(self):
        self.a = randint(0, 11)
        self.b = randint(0, 11)
        self.s = symbols[randint(0, len(symbols) - 1)]

        match self.s:
            case "+":
                self.r = self.a + self.b
            case "-":
                self.r = self.a - self.b
            case "*":
                self.r = self.a * self.b
            case "/":
                self.r = self.a / self.b

equations = {}
points = {}
usernames = {}
connection_index = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((argv[1], int(argv[2])))
sock.listen(int(argv[3]))

class Connection:
    def __init__(self, d: tuple[socket.socket, socket.AddressFamily]):
        self.sock = d[0]
        self.ip = d[1]
        self.id = connection_index

        self.auth = False
        self.points = 0
        self.username = "None"
    def send(self, d):
        try:
            self.sock.send(json.dumps(d).encode())
            return True
        except:
            print(f"Error sending data {d}, disconnecting client {self.username}({self.id})")
            self.sock.close()
            
            return False
    def recv(self):
        try:
            return json.loads(self.sock.recv(1024).decode())
        except:
            print(f"Error recieving data, disconnecting client {self.username}({self.id})")
            self.sock.close()

            return False
    def handle(self):
        global connection_index
        global usernames
        global points

        print(f"Handling client {self.id}")

        equations[f'{self.id}'] = equation(1, 1)
        usernames[f'{self.id}'] = self.username
        points[f'{self.id}'] = 0

        while True:
            if not self.auth:
                d = self.recv()

                if not d:
                    break

                if d['op'] == 0:
                    self.username = d['d']['username']
                    usernames[f'{self.id}'] = self.username
                    print(f"Client {self.id} authorized with the username {self.username}")

                    self.auth = True
            else:
                if not self.send({"op": 1, "d": {"sum": equations[f'{self.id}'].e()}}):
                    break

                d = self.recv()

                if not d:
                    break

                if d['op'] == 1:
                    m = equations[f'{self.id}'].r == d['d']['answer']

                    if not self.send({"op": 2, "d": {"correct": m}}):
                        break

                    if m:
                        equations[f'{self.id}'].n()
                        points[f'{self.id}'] += 1
        
def handle_connections():
    global connection_index

    while True:
        Thread(target=Connection(sock.accept()).handle, daemon=True).start()
        connection_index += 1

Thread(target=handle_connections, daemon=True).start()

print("Starting game!")

while True:
    for i in equations:
        print(end=f"{usernames[i]}({i}): {points[f'{i}']}({equations[i].e()}), ")

    print(end="\r")
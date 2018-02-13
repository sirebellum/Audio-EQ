import socket

class wavstream:
    def __init__(self, port, ipaddress):
        self.UDP_IP = ipaddress #IP of network interface to be used
        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP
        self.UDP_PORT = port
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.data = list()
        self.kill_process = False
        
    def start(self):
    
        while not self.kill_process:
            self.data.append(self.sock.recv(1764)) # buffer size is 1024 bytes

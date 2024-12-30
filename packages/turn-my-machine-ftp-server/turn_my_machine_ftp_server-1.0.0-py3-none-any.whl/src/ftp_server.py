import os
import socket
import threading

class FTPServer:
    def __init__(self, host='0.0.0.0', port=21, root_dir=None):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root_dir = root_dir or os.getcwd()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"FTP server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        client_socket.sendall(b"220 Welcome to the custom FTP server\r\n")
        current_dir = self.root_dir

        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            print(f"Command received: {data}")
            
            if data.startswith("USER"):
                client_socket.sendall(b"331 User name okay, need password\r\n")
            elif data.startswith("PASS"):
                client_socket.sendall(b"230 User logged in, proceed\r\n")
            elif data.startswith("PWD"):
                client_socket.sendall(f'257 "{current_dir}" is the current directory\r\n'.encode())
            elif data.startswith("LIST"):
                files = "\r\n".join(os.listdir(current_dir))
                client_socket.sendall(b"150 Here comes the directory listing\r\n")
                client_socket.sendall(files.encode() + b"\r\n226 Directory send okay\r\n")
            elif data.startswith("QUIT"):
                client_socket.sendall(b"221 Goodbye\r\n")
                client_socket.close()
                break
            else:
                client_socket.sendall(b"502 Command not implemented\r\n")

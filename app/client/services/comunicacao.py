# comunicacao.py - encapsula a comunicação socket do cliente

import socket

class ClienteSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        self.sock.connect((self.host, self.port))

    def enviar(self, mensagem):
        self.sock.sendall(mensagem.encode())

    def receber(self, buffer=1024):
        return self.sock.recv(buffer).decode()

    def fechar(self):
        self.sock.close()

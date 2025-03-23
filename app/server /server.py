# server/server.py
import socket
import shutil

if shutil.which("python"):
    print("Python encontrado!")
else:
    print("Python não encontrado!")


HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000        # Porta do servidor

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"Servidor rodando na porta {PORT}...")

    while True:
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")
        
        data = conn.recv(1024).decode()
        if data == "START":
            response = "Carregamento iniciado!"
        elif data == "STOP":
            response = "Carregamento encerrado!"
        else:
            response = "Comando inválido!"

        conn.send(response.encode())
        conn.close()

if __name__ == "__main__":
    main()

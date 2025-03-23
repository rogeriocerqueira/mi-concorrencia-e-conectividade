# client/client.py
import socket

HOST = 'server'  # Nome do serviço dentro do Docker Compose
PORT = 5000      # Porta do servidor

def send_command(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(command.encode())

    response = client.recv(1024).decode()
    print(f"Resposta do servidor: {response}")

    client.close()

if __name__ == "__main__":
    while True:
        cmd = input("Digite START para iniciar o carregamento ou STOP para parar: ")
        if cmd.upper() in ["START", "STOP"]:
            send_command(cmd.upper())
        else:
            print("Comando inválido. Tente novamente.")

import socket

HOST = 'server'  # Nome do serviço dentro do Docker Compose
PORT = 5000      # Porta do servidor

def send_command(command):
    """Envia um comando ao servidor e exibe a resposta."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.send(command.encode())

            response = client.recv(1024).decode()
            print(f"Resposta do servidor: {response}")
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Verifique se ele está rodando.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema: {e}")

if __name__ == "__main__":
    print("Cliente conectado. Digite 'START' para iniciar o carregamento, 'STOP' para parar ou 'EXIT' para sair.")

    while True:
        cmd = input("> ").strip().upper()

        if cmd == "EXIT":
            print("Saindo do cliente...")
            break
        elif cmd in ["START", "STOP"]:
            send_command(cmd)
        else:
            print("Comando inválido. Use 'START', 'STOP' ou 'EXIT'.")

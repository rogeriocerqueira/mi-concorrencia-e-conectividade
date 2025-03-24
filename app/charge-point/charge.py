import socket
import time

HOST = 'server'  # Nome do serviço dentro do Docker Compose
PORT = 5000      # Porta do servidor

def connect_to_server():
    """Estabelece conexão com o servidor e espera comandos."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as charge_point:
            charge_point.connect((HOST, PORT))
            print("[CONECTADO] Ponto de carregamento pronto para receber comandos.")

            while True:
                charge_point.send("STATUS".encode())  # Pergunta ao servidor se há comandos
                response = charge_point.recv(1024).decode()
                
                if response == "START":
                    print("[CARREGANDO] Iniciando o carregamento do veículo...")
                    time.sleep(5)  # Simula o tempo de carregamento
                    print("[COMPLETO] Carregamento finalizado.")
                    charge_point.send("COMPLETE".encode())  # Informa ao servidor que terminou
                elif response == "STOP":
                    print("[PARADO] Carregamento interrompido.")
                    break
                else:
                    print("[AGUARDANDO] Nenhum comando recebido.")
                    time.sleep(2)  # Aguarda antes de perguntar novamente
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Verifique se ele está rodando.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema: {e}")

if __name__ == "__main__":
    print("[INICIANDO] Ponto de carregamento online.")
    connect_to_server()

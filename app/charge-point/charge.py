import socket
import time
from services.controle import aceitar_carregamento
from services.monitoramento import logar_evento


HOST = 'server'  # Nome do serviço no Docker Compose
PORT = 5000      # Porta usada pelo servidor

def connect_to_server():
    """Conecta ao servidor repetidamente para verificar comandos."""
    print("[INICIANDO] Ponto de carregamento online.")
    
    while True:
        try:
            # Envia STATUS
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as charge_point:
                charge_point.connect((HOST, PORT))
                print("[CONECTADO] Verificando instruções do servidor...")
                charge_point.send("STATUS".encode())
                response = charge_point.recv(1024).decode()

            # Lida com a resposta
            if aceitar_carregamento():
                print("[CARREGANDO] Iniciando o carregamento do veículo...")
                time.sleep(5)
                print("[COMPLETO] Carregamento finalizado.")
                logar_evento("Carregamento concluído com sucesso.")

                # Envia mensagem de COMPLETE ao servidor
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cp_complete:
                    cp_complete.connect((HOST, PORT))
                    cp_complete.send("COMPLETE".encode())
            else:
                print("[NEGADO] Carregamento não autorizado pelo controle.")


        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar ao servidor. Verifique se ele está rodando.")
            time.sleep(2)
        except Exception as e:
            print(f"[ERRO] Ocorreu um problema: {e}")
            time.sleep(2)

if __name__ == "__main__":
    connect_to_server()

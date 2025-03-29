# charge.py - atualizado com reconexão automática se o servidor não estiver pronto

import socket
import time
from services import controle, monitoramento

HOST = "server"  # nome do serviço no docker-compose
PORT = 5000
NOME_CHARGE_POINT = "charge-point-1"  # mudar conforme o container

def connect_to_server():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(f"CHARGE-POINT:{NOME_CHARGE_POINT}".encode())
                print(f"[{NOME_CHARGE_POINT.upper()}] Conectado ao servidor e aguardando comandos.")

                while True:
                    comando = s.recv(1024).decode().strip()
                    if comando == "START":
                        if controle.horario_permitido():
                            monitoramento.logar_evento("Carregamento autorizado.")
                            monitoramento.logar_evento("Iniciando o carregamento do veículo...")
                            time.sleep(3)
                            monitoramento.logar_evento("Carregamento finalizado.")
                        else:
                            monitoramento.logar_evento("Fora do horário permitido. Carregamento negado.")
                    else:
                        monitoramento.logar_evento(f"Comando não reconhecido: {comando}")
        
        except Exception as e:
            print(f"[{NOME_CHARGE_POINT.upper()}] ERRO: {e}. Tentando novamente em 5s...")
            time.sleep(5)

if __name__ == "__main__":
    connect_to_server()
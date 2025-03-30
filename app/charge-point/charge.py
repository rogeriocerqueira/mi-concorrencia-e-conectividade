# charge.py - corrigido para não sobrescrever NOME_CHARGE_POINT

import socket
import time
import os
from services import controle, monitoramento

HOST = "server"
PORT = 5000
NOME_CHARGE_POINT = os.getenv("NOME_CHARGE_POINT", "charge-point-1")

def connect_to_server():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Tenta se conectar ao servidor
                while True:
                    try:
                        s.connect((HOST, PORT))
                        break
                    except ConnectionRefusedError:
                        print(f"[{NOME_CHARGE_POINT.upper()}] Servidor não está pronto. Tentando novamente em 2s...")
                        time.sleep(2)

                s.send(f"CHARGE-POINT:{NOME_CHARGE_POINT}".encode())
                print(f"[{NOME_CHARGE_POINT.upper()}] Conectado ao servidor e aguardando comandos.")

                while True:
                    comando = s.recv(1024).decode().strip()
                    if comando == "START":
                        if controle.horario_permitido():
                            monitoramento.logar_evento("Carregamento autorizado.", origem=NOME_CHARGE_POINT)
                            monitoramento.logar_evento("Iniciando o carregamento do veículo...", origem=NOME_CHARGE_POINT)
                            time.sleep(3)
                            monitoramento.logar_evento("Carregamento finalizado.", origem=NOME_CHARGE_POINT)

                            # Envia COMPLETE para o servidor
                            try:
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
                                    cs.connect((HOST, PORT))
                                    cs.send(f"COMPLETE:{NOME_CHARGE_POINT}".encode())
                            except Exception as e:
                                print(f"[{NOME_CHARGE_POINT.upper()}] ERRO ao enviar COMPLETE: {e}")
                        else:
                            monitoramento.logar_evento("Fora do horário permitido. Carregamento negado.", origem=NOME_CHARGE_POINT)
                    else:
                        monitoramento.logar_evento(f"Comando não reconhecido: {comando}", origem=NOME_CHARGE_POINT)

        except Exception as e:
            print(f"[{NOME_CHARGE_POINT.upper()}] ERRO: {e}. Tentando novamente em 5s...")
            time.sleep(5)

if __name__ == "__main__":
    connect_to_server()

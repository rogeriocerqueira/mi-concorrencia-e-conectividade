# server.py - logs agora usam origem "SERVER" para o monitoramento

import socket
import threading
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

posicoes_clientes = {}
conexoes_charge_points = {}
postos_de_recarga = {
    "charge-point-1": 10,
    "charge-point-2": 50,
    "charge-point-3": 90
}

def log_evento(texto):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] [SERVER] {texto}"
    print(linha)
    with open("log.txt", "a") as f:
        f.write(linha + "\n")

def posto_mais_proximo(posicao_cliente):
    menor_dist = float('inf')
    escolhido = None
    for nome, pos in postos_de_recarga.items():
        dist = abs(posicao_cliente - pos)
        if dist < menor_dist:
            menor_dist = dist
            escolhido = nome
    return escolhido

def handle_client(conn, addr):
    log_evento(f"[NOVA CONEXÃO] Conectado a {addr}")

    try:
        identificacao = conn.recv(1024).decode().strip()

        if identificacao.startswith("CHARGE-POINT:"):
            nome = identificacao.split(":")[1]
            conexoes_charge_points[nome] = conn
            log_evento(f"[REGISTRO] {nome} registrado como charge-point.")
            while True:
                time.sleep(1)

        elif identificacao.startswith("COMPLETE:"):
            nome = identificacao.split(":")[1]
            log_evento(f"[FINALIZADO] {nome} completou o carregamento.")

        else:
            while True:
                data = identificacao if identificacao else conn.recv(1024).decode().strip()
                identificacao = None

                if not data:
                    break

                if data == "START":
                    if addr in posicoes_clientes:
                        posicao = posicoes_clientes[addr]
                        posto = posto_mais_proximo(posicao)
                        log_evento(f"[DECISÃO] Cliente {addr} em {posicao} -> {posto}")
                        if posto in conexoes_charge_points:
                            try:
                                conexoes_charge_points[posto].send("START".encode())
                                response = f"Instrução enviada para {posto}"
                            except:
                                response = f"Erro ao enviar comando para {posto}"
                        else:
                            response = f"{posto} não está conectado ao servidor."
                    else:
                        response = "Posição do cliente desconhecida. Envie POSICAO antes."

                elif data == "STOP":
                    response = "Carregamento encerrado pelo cliente."

                elif data.startswith("POSICAO:"):
                    try:
                        pos = int(data.split(":")[1])
                        posicoes_clientes[addr] = pos
                        log_evento(f"[POSIÇÃO] {addr} está na posição {pos}")
                        response = "Posição registrada"
                    except:
                        response = "Formato inválido. Use POSICAO:<número>"
                else:
                    response = "Comando inválido!"

                conn.send(response.encode())

    except Exception as e:
        log_evento(f"[ERRO] Problema com {addr}: {e}")

    finally:
        conn.close()
        log_evento(f"[DESCONECTADO] {addr} desconectado.")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log_evento(f"[SERVIDOR RODANDO] Porta {PORT}...")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()

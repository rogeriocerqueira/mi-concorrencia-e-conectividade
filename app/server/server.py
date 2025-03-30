# server.py - agora responde ao cliente com o posto mais próximo em tempo real

import socket
import threading
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

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
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            if data.startswith("POSICAO:"):
                try:
                    pos = int(data.split(":")[1])
                    log_evento(f"[POSIÇÃO] {addr} está na posição {pos}")
                    posto = posto_mais_proximo(pos)
                    log_evento(f"[RESPOSTA] Cliente {addr} -> {posto}")
                    conn.send(posto.encode())
                except:
                    conn.send("ERRO: posição inválida".encode())
            else:
                conn.send("Comando não reconhecido".encode())

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

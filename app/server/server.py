# server.py - atualizado com suporte a reservas

import socket
import threading
import time
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000

postos_de_recarga = {
    "charge-point-1": 10,
    "charge-point-2": 50,
    "charge-point-3": 90
}

LOG_PATH = "app/server/log.txt"
RESERVAS_PATH = "app/server/reservas.txt"

# Utilitário de log

def log_evento(texto):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] [SERVER] {texto}"
    print(linha, flush=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(linha + "\n")

# Verificar posto mais próximo

def posto_mais_proximo(posicao_cliente):
    menor_dist = float('inf')
    escolhido = None
    for nome, pos in postos_de_recarga.items():
        dist = abs(posicao_cliente - pos)
        if dist < menor_dist:
            menor_dist = dist
            escolhido = nome
    return escolhido

# Verifica se o posto está disponível no horário

def verificar_disponibilidade(data, hora, posto):
    if not os.path.exists(RESERVAS_PATH):
        return True
    with open(RESERVAS_PATH, "r") as f:
        for linha in f:
            linha = linha.strip()
            if linha == f"{data},{hora},{posto}":
                return False
    return True

# Salva a reserva

def registrar_reserva(data, hora, posto):
    os.makedirs(os.path.dirname(RESERVAS_PATH), exist_ok=True)
    with open(RESERVAS_PATH, "a") as f:
        f.write(f"{data},{hora},{posto}\n")

# Cliente handler

def handle_client(conn, addr):
    log_evento(f"[NOVA CONEXÃO] Conectado a {addr}")
    conn.send("Conectado ao servidor. Envie POSICAO:<número> ou RESERVAR:<dd/mm/yyyy>:<HH:MM>:<posto>".encode())
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
                    mensagem = f"{posto} (posição: {postos_de_recarga[posto]})"
                    conn.send(mensagem.encode())
                except ValueError:
                    conn.send("ERRO: posição inválida".encode())

            elif data.startswith("RESERVAR:"):
                try:
                    _, data_res, hora_res, posto = data.split(":")
                    if verificar_disponibilidade(data_res, hora_res, posto):
                        registrar_reserva(data_res, hora_res, posto)
                        mensagem = f"Reserva confirmada para {posto} às {hora_res} em {data_res}."
                        log_evento(f"[RESERVA] {addr} -> {mensagem}")
                        conn.send(mensagem.encode())
                    else:
                        mensagem = f"Posto {posto} já reservado nesse horário."
                        log_evento(f"[RESERVA NEGADA] {addr} -> {mensagem}")
                        conn.send(mensagem.encode())
                except Exception as e:
                    conn.send(f"ERRO ao processar reserva: {e}".encode())

            else:
                conn.send("Comando não reconhecido. Use POSICAO:<número> ou RESERVAR:<data>:<hora>:<posto>".encode())

    except Exception as e:
        log_evento(f"[ERRO] Problema com {addr}: {e}")

    finally:
        conn.close()
        log_evento(f"[DESCONECTADO] {addr} desconectado.")

# Iniciar servidor

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
    log_evento("Servidor iniciado com sucesso.")
    start_server()

# client.py - atualizado para envio automático da posição a cada 60 segundos

import time
import random
from services.comunicacao import ClienteSocket

HOST = "server"
PORT = 5000

cliente = ClienteSocket(HOST, PORT)

def enviar_posicao_automatica():
    try:
        cliente.conectar()
        print("[CLIENTE] Conectado ao servidor. Iniciando envio automático de posição...")

        while True:
            posicao = random.randint(0, 100)
            cliente.enviar(f"POSICAO:{posicao}")
            resposta = cliente.receber()
            print(f"[CLIENTE] Posição enviada: {posicao} | Posto mais próximo: {resposta}")
            time.sleep(60)  # Aguarda 60 segundos

    except Exception as e:
        print("[ERRO] Falha na conexão com o servidor:", e)
    finally:
        cliente.fechar()

if __name__ == "__main__":
    try:
        enviar_posicao_automatica()
    except KeyboardInterrupt:
        print("\n[CLIENTE] Encerrando cliente.")

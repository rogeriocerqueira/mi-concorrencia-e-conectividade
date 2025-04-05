# client.py - atualizado com envio de reservas manuais via terminal

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
            print(f"[CLIENTE] Posição enviada: {posicao} | ⛽ Posto mais próximo: {resposta}")
            time.sleep(60)

    except Exception as e:
        print("[ERRO] Falha na conexão com o servidor:", e)
    finally:
        cliente.fechar()

def realizar_reserva():
    try:
        cliente.conectar()
        print("[CLIENTE] Modo reserva iniciado.")
        while True:
            entrada = input("Digite RESERVAR:<data>:<hora>:<posto> ou 'sair': ").strip()
            if entrada.lower() == "sair":
                break
            if entrada.startswith("RESERVAR:"):
                cliente.enviar(entrada)
                resposta = cliente.receber()
                print(f"[CLIENTE] {resposta}")
            else:
                print("[CLIENTE] Formato inválido. Use: RESERVAR:dd/mm/yyyy:HH:MM:charge-point-x")

    except Exception as e:
        print("[ERRO] Falha na reserva:", e)
    finally:
        cliente.fechar()

if __name__ == "__main__":
    print("[CLIENTE] 1 - Enviar posição automática\n[CLIENTE] 2 - Fazer reserva manual")
    opcao = input("Escolha uma opção: ").strip()
    if opcao == "1":
        enviar_posicao_automatica()
    elif opcao == "2":
        realizar_reserva()
    else:
        print("[CLIENTE] Opção inválida.")
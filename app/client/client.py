# client.py - cliente principal (refatorado)

import json
import time
from services.bateria import GerenciadorBateria
from services.comunicacao_rest import ClienteREST
from services.comunicacao_mqtt import ClienteMQTT

# Carrega configurações
with open("config/settings.json") as f:
    config = json.load(f)

modo = config["modo"]
cliente_id = config["cliente_id"]
posicao = config["posicao_inicial"]

# Inicializa o modo de comunicação
comunicador = ClienteREST(cliente_id) if modo == "REST" else ClienteMQTT(cliente_id)

# Inicializa o gerenciador de bateria e reserva
bateria = GerenciadorBateria(cliente_id, comunicador)

print(f"[CLIENTE] Iniciando com modo {modo}...")

while True:
    print(f"[CLIENTE] Posição atual: {posicao} | Bateria: {bateria.nivel}%")

    comunicador.enviar_posicao(posicao)
    bateria.verificar_bateria()

    time.sleep(60)

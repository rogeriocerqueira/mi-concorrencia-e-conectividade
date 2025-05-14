from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import os
import json
import time
import threading

app = Flask(__name__)

# Estado atual deste servidor (ex: BA)
POSTO_LOCAL = "MA"

# Configuração do broker MQTT
broker_address = "broker_ma"
broker_port = 1885
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="server_ma", protocol=mqtt.MQTTv311)
client.connect(broker_address, broker_port, 60)

# Pasta e arquivo para salvar reservas
PASTA_RESERVAS = "./dados"
ARQUIVO_RESERVAS = os.path.join(PASTA_RESERVAS, "reservas.json")

# Estados válidos
ESTADOS_VALIDOS = {"BA", "SE", "MA"}

# Cria pasta e arquivo se não existirem
os.makedirs(PASTA_RESERVAS, exist_ok=True)
if not os.path.exists(ARQUIVO_RESERVAS):
    with open(ARQUIVO_RESERVAS, "w") as f:
        json.dump({}, f)

def carregar_reservas():
    with open(ARQUIVO_RESERVAS, "r") as f:
        return json.load(f)

def salvar_reservas(reservas):
    with open(ARQUIVO_RESERVAS, "w") as f:
        json.dump(reservas, f)

def liberar_reserva(horario):
    time.sleep(120)
    reservas = carregar_reservas()
    if horario in reservas:
        print(f"[LIBERAÇÃO AUTOMÁTICA] Horário {horario} liberado.")
        del reservas[horario]
        salvar_reservas(reservas)

@app.route('/reservar', methods=['POST'])
def reservar():
    dados = request.get_json()

    cliente = dados.get('cliente')
    horario = dados.get('horario')
    origem = dados.get('origem')
    destino = dados.get('destino')

    if not cliente or not horario or not origem or not destino:
        return jsonify({"error": "Campos 'cliente', 'horario', 'origem' e 'destino' são obrigatórios."}), 400

    if origem not in ESTADOS_VALIDOS:
        return jsonify({"error": f"Origem '{origem}' inválida. Use apenas: {list(ESTADOS_VALIDOS)}"}), 400
    if destino not in ESTADOS_VALIDOS:
        return jsonify({"error": f"Destino '{destino}' inválido. Use apenas: {list(ESTADOS_VALIDOS)}"}), 400

    # Impedir reserva em posto diferente do servidor atual
    if origem != POSTO_LOCAL:
        return jsonify({"error": f"Este servidor só atende solicitações com origem '{POSTO_LOCAL}'."}), 403

    reservas = carregar_reservas()
    if horario in reservas:
        return jsonify({"error": f"Horário {horario} já está reservado por {reservas[horario]['cliente']}"}), 409

    reservas[horario] = {
        "cliente": cliente,
        "origem": origem,
        "destino": destino,
        "timestamp": time.time()
    }
    salvar_reservas(reservas)

    payload = f"Reserva para {cliente} de {origem} para {destino} às {horario}"
    topic = f"reserva/{POSTO_LOCAL}"
    client.publish(topic, payload)

    threading.Thread(target=liberar_reserva, args=(horario,)).start()

    return jsonify({"message": "Reserva realizada com sucesso.", "topico": topic, "payload": payload}), 200


@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    dados = request.get_json()
    posto = dados.get('posto')
    status = dados.get('status')

    if not posto or not status:
        return jsonify({"error": "Campos 'posto' e 'status' são obrigatórios."}), 400

    print(f"[STATUS] Posto {posto} está agora '{status}'")

    return jsonify({"message": "Status recebido com sucesso."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

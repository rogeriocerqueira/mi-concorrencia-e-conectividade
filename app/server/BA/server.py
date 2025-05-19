from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import os
import json
import time
import threading

app = Flask(__name__)

# Estado atual deste servidor (ex: BA)
POSTO_LOCAL = "BA"

# Configuração do broker MQTT
broker_address = "broker_ba"
broker_port = 1884
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="server_ba", protocol=mqtt.MQTTv311)
client.connect(broker_address, broker_port, 60)

# Pasta e arquivo para salvar reservas
PASTA_RESERVAS = "./dados"
ARQUIVO_RESERVAS = os.path.join(PASTA_RESERVAS, "reservas.json")

# Estados válidos
ESTADOS_VALIDOS = {"BA", "SE", "MA"}

# Postos por estado
POSTOS_ESTADO = {
    "BA": ["posto1-ba", "posto2-ba", "posto3-ba", "posto4-ba", "posto5-ba"],
    "MA": ["posto1-ma", "posto2-ma", "posto3-ma"],
    "SE": ["posto1-se", "posto2-se"]
}

# Dicionário para armazenar respostas MQTT de disponibilidade
respostas_disponibilidade = {}
lock = threading.Lock()

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

# Handler para resposta de disponibilidade via MQTT
def on_message(client, userdata, msg):
    global respostas_disponibilidade
    try:
        data = json.loads(msg.payload.decode())
        posto = data["posto"]
        horario = data["horario"]
        disponivel = data["disponivel"]

        key = (posto, horario)

        with lock:
            respostas_disponibilidade[key] = disponivel
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

client.on_message = on_message
client.subscribe("resposta_disponibilidade/#")  # escuta todas as respostas
client.loop_start()

# Verifica os postos disponíveis via MQTT
def verificar_postos_disponiveis(horario):
    global respostas_disponibilidade
    respostas_disponibilidade = {}

    postos_escolhidos = {}

    # Publica verificação para todos os postos
    for estado, postos in POSTOS_ESTADO.items():
        for posto in postos:
            topico = f"verificar_disponibilidade/{posto}"
            payload = json.dumps({"horario": horario})
            client.publish(topico, payload)

    # Espera respostas por até 5 segundos
    timeout = time.time() + 5
    while time.time() < timeout:
        with lock:
            for estado, postos in POSTOS_ESTADO.items():
                if estado not in postos_escolhidos:
                    for posto in postos:
                        key = (posto, horario)
                        if respostas_disponibilidade.get(key):
                            postos_escolhidos[estado] = posto
                            break
        if len(postos_escolhidos) == 3:
            break
        time.sleep(0.2)

    return postos_escolhidos if len(postos_escolhidos) == 3 else None

@app.route('/reserva', methods=['POST'])
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

    if origem != POSTO_LOCAL:
        return jsonify({"error": f"Este servidor só atende solicitações com origem '{POSTO_LOCAL}'."}), 403

    reservas = carregar_reservas()
    if horario in reservas:
        return jsonify({"error": f"Horário {horario} já está reservado por {reservas[horario]['cliente']}"}), 409

    # Verifica disponibilidade em todos os estados
    postos_escolhidos = verificar_postos_disponiveis(horario)
    if not postos_escolhidos:
        return jsonify({"error": "Não foi possível reservar. Todos os estados devem ter ao menos 1 posto livre."}), 409

    # Envia reserva para os postos encontrados
    for estado, posto in postos_escolhidos.items():
        topico = f"reserva/{posto}"
        payload = {
            "cliente": cliente,
            "horario": horario,
            "posto": posto
        }
        client.publish(topico, json.dumps(payload))

    # Também salva a própria reserva (BA)
    reservas[horario] = {
        "cliente": cliente,
        "posto": postos_escolhidos["BA"],
        "origem": origem,
        "destino": destino,
        "timestamp": time.time()
    }
    salvar_reservas(reservas)

    threading.Thread(target=liberar_reserva, args=(horario,)).start()

    return jsonify({
        "message": "Reserva confirmada.",
        "postos_reservados": postos_escolhidos
    }), 200

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

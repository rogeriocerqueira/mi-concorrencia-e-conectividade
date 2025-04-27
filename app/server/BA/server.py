from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do broker MQTT
broker_address = "broker_ba"
broker_port = 1884

# Inicializa o cliente MQTT
client = mqtt.Client(client_id="server_ba", protocol=mqtt.MQTTv311, callback_api_version=5)
client.connect(broker_address, broker_port, 60)

@app.route('/reservar', methods=['POST'])
def reservar():
    """Rota para criar uma reserva e enviar via MQTT."""
    dados = request.get_json()

    posto = dados.get('posto')
    cliente = dados.get('cliente')
    horario = dados.get('horario')

    if not posto or not cliente or not horario:
        return jsonify({"error": "Campos 'posto', 'cliente' e 'horario' são obrigatórios."}), 400

    payload = f"Reserva para {cliente} no posto {posto} às {horario}"
    topic = f"reserva/{posto}"

    client.publish(topic, payload)

    return jsonify({"message": "Reserva enviada via MQTT.", "topic": topic, "payload": payload}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

broker_address = "broker_se"
broker_port = 1885

client = mqtt.Client("server_ba")
client.connect(broker_address, broker_port, 60)

@app.route('/reservar', methods=['POST'])
def reservar():
    dados = request.json
    posto = dados.get('posto')
    cliente = dados.get('cliente')
    horario = dados.get('horario')

    payload = f"Reserva para {cliente} no posto {posto} às {horario}"
    topic = f"reserva/{posto}"
    
    client.publish(topic, payload)
    return jsonify({"message": "Reserva enviada via MQTT", "topic": topic, "payload": payload})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

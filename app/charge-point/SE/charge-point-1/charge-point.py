import paho.mqtt.client as mqtt
import time
import requests

broker_address = "broker_se"
broker_port = 1887
client_id = "charge-point-1"

server_address = "server_se"
server_port = 5002
server_endpoint = f"http://{server_address}:{server_port}/atualizar_status"

# Usando API de callback versão 2
client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker_ba", 1883, 60)

def notify_server(status):
    data = {"posto": client_id, "status": status}
    try:
        response = requests.post(server_endpoint, json=data)
        print(f"[HTTP] Status enviado ao servidor: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[HTTP] Erro ao enviar status: {e}")

def publish_status(status):
    topic = f"status/{client_id}"
    client.publish(topic, status)
    print(f"[MQTT] Publicando no tópico {topic}: {status}")
    notify_server(status)

# Assinatura atualizada do callback (versão 2.0)
def on_message(client, userdata, message, properties=None):
    comando = str(message.payload.decode("utf-8"))
    print(f"[MQTT] Comando recebido: {comando}")
    if comando == "start":
        publish_status("Carregando")
    elif comando == "stop":
        publish_status("Livre")
    else:
        print("[MQTT] Comando desconhecido.")

# Definir callback de mensagem
client.subscribe(f"command/{client_id}")
client.on_message = on_message

# Publicar status inicial
publish_status("Livre")

# Iniciar loop MQTT
client.loop_start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Encerrando charge-point...")
    client.loop_stop()

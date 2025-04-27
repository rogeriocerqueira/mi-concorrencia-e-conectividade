import paho.mqtt.client as mqtt
import time

# Configurações
broker_address = "broker_ba"  # Atenção: alterar conforme a região!
broker_port = 1883
client_id = "charge-point-3"  # Nome do posto de recarga

# Inicializa o cliente MQTT
client = mqtt.Client(client_id)

# Conecta no broker
client.connect(broker_address, broker_port, 60)

def publish_status(status):
    topic = f"status/{client_id}"
    client.publish(topic, status)
    print(f"Publicando no tópico {topic}: {status}")

# Quando receber um comando
def on_message(client, userdata, message):
    comando = str(message.payload.decode("utf-8"))
    print(f"Recebido comando: {comando}")

    if comando == "start":
        publish_status("Carregando")
    elif comando == "stop":
        publish_status("Livre")
    else:
        print("Comando desconhecido.")

# Inscreve para escutar comandos
client.subscribe(f"command/{client_id}")
client.on_message = on_message

# Publica status inicial
publish_status("Livre")

# Inicia o loop para escutar mensagens
client.loop_start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Encerrando charge-point...")
    client.loop_stop()

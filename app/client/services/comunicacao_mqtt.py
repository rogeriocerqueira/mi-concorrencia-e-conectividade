# comunicacao_mqtt.py - cliente MQTT

import paho.mqtt.client as mqtt
from services.reserva import Reserva
import json

class ClienteMQTT:
    def __init__(self, cliente_id):
        self.cliente_id = cliente_id
        self.broker = "mosquitto"  # Nome do serviço do broker MQTT no docker-compose
        self.porta = 1883
        self.topico_posicao = f"clientes/{cliente_id}/posicao"
        self.topico_reserva = f"clientes/{cliente_id}/reserva"

        self.client = mqtt.Client()
        self.client.connect(self.broker, self.porta, 60)

    def enviar_posicao(self, posicao):
        try:
            payload = str(posicao)
            self.client.publish(self.topico_posicao, payload)
            print(f"[MQTT] Posição publicada: {payload}")
        except Exception as e:
            print(f"[MQTT] Erro ao publicar posição: {e}")

    def solicitar_reserva(self):
        reserva = Reserva(self.cliente_id, "charge-point-1", "21/04/2025", "14:00")
        try:
            payload = json.dumps(reserva.to_dict())
            self.client.publish(self.topico_reserva, payload)
            print("[MQTT] Solicitação de reserva publicada.")
        except Exception as e:
            print(f"[MQTT] Erro ao solicitar reserva: {e}")

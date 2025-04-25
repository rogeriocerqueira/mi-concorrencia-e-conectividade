# comunicacao_rest.py - cliente REST

import requests
from services.reserva import Reserva

import os



class ClienteREST:
    def __init__(self, cliente_id):
        self.cliente_id = cliente_id
        self.base_url = os.getenv("SERVER_URL", "http://127.0.0.1:5000")  # valor padrão

    def enviar_posicao(self, posicao):
        try:
            resposta = requests.post(f"{self.base_url}/posicao", json={
                "cliente_id": self.cliente_id,
                "posicao": posicao
            })
            print(f"[REST] Resposta do servidor: {resposta.text}")
        except Exception as e:
            print(f"[REST] Erro ao enviar posição: {e}")

    def solicitar_reserva(self):
        reserva = Reserva(self.cliente_id, "charge-point-1", "21/04/2025", "14:00")
        try:
            resposta = requests.post(f"{self.base_url}/reserva", json=reserva.to_dict())
            print(f"[REST] Reserva: {resposta.text}")
        except Exception as e:
            print(f"[REST] Erro ao solicitar reserva: {e}")

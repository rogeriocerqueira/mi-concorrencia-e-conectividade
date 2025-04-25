# reserva.py - lógica de criação de reserva

class Reserva:
    def __init__(self, cliente_id, posto, data, hora):
        self.cliente_id = cliente_id
        self.posto = posto
        self.data = data
        self.hora = hora

    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "posto": self.posto,
            "data": self.data,
            "hora": self.hora
        }

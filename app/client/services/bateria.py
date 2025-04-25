# bateria.py - controle de bateria e reserva

class GerenciadorBateria:
    def __init__(self, cliente_id, comunicador):
        self.nivel = 100
        self.cliente_id = cliente_id
        self.comunicador = comunicador

    def verificar_bateria(self):
        self.nivel = max(0, self.nivel - 10)
        if self.nivel <= 20:
            print("[CLIENTE] Bateria crítica! Solicitando reserva...")
            self.comunicador.solicitar_reserva()

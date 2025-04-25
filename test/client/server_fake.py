# server_fake.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/posicao", methods=["POST"])
def posicao():
    dados = request.get_json()
    print(f"📍 Cliente {dados['cliente_id']} na posição {dados['posicao']}")
    return "Posição recebida", 200

@app.route("/reserva", methods=["POST"])
def reserva():
    dados = request.get_json()
    print(f"📅 Reserva solicitada: {dados}")
    return "Reserva recebida", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

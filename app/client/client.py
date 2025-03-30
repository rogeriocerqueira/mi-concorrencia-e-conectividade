# client.py - atualizado para usar ClienteSocket

from services.comunicacao import ClienteSocket
from services.localizacao import posicao_atual

HOST = "server"
PORT = 5000

cliente = ClienteSocket(HOST, PORT)


def enviar_posicao():
    cliente.enviar(f"POSICAO:{posicao_atual}")
    print(cliente.receber())


def send_command(cmd):
    cliente.enviar(cmd)
    resposta = cliente.receber()
    print("Resposta do servidor:", resposta)


def main():
    try:
        cliente.conectar()
        print("Cliente conectado. Digite 'START' para iniciar o carregamento, 'STOP' para parar ou 'EXIT' para sair.")

        while True:
            cmd = input("> ").strip().upper()

            if cmd == "EXIT":
                print("Saindo do cliente...")
                break
            elif cmd.startswith("POSICAO:") or cmd in ["START", "STOP"]:
                send_command(cmd)
            else:
                print("Comando inválido. Use 'POSICAO:<número>', 'START', 'STOP' ou 'EXIT'.")

    except Exception as e:
        print("Erro ao se conectar com o servidor:", e)
    finally:
        cliente.fechar()


if __name__ == "__main__":
    main()

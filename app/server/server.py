import socket
import threading

posicoes_clientes = {}  # Mapeia addr do cliente para posição
postos_de_recarga = {
    "charge-point-1": 10,
    "charge-point-2": 50,
    "charge-point-3": 90
}


HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000        # Porta do servidor
posicoes_clientes = {}  # Ex: {("172.20.0.4", 34423): 42}

def handle_client(conn, addr):
    """Lida com um cliente conectado."""
    print(f"[NOVA CONEXÃO] Conectado a {addr}")

    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            response = "Nenhum comando recebido!"
        elif data == "START":
            if addr in posicoes_clientes:
                posicao = posicoes_clientes[addr]
                posto_escolhido = posto_mais_proximo(posicao)
                print(f"[DECISÃO] Cliente {addr} está em {posicao}. Posto mais próximo: {posto_escolhido}")
                response = f"Direcionado para {posto_escolhido}"
            else: 
                response = "Posição do cliente desconhecida. Envie POSICAO antes do START."

        elif data == "STOP":
            response = "Carregamento encerrado!"
        
        elif data.startswith("POSICAO:"):
            try:
                posicao_cliente = int(data.split(":")[1])
                posicoes_clientes[addr] = posicao_cliente
                print(f"[POSIÇÃO] {addr} está na posição {posicao_cliente}")
                response = "Posição registrada com sucesso"
            except ValueError:
                response = "Posição inválida"

        else:
            response = "Comando inválido!"

        conn.send(response.encode())
    except Exception as e:
        print(f"[ERRO] Problema ao processar conexão de {addr}: {e}")
    finally:
        conn.close()
        print(f"[DESCONECTADO] {addr} desconectado.")

def main():
    """Inicia o servidor."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"[SERVIDOR RODANDO] O servidor está rodando na porta {PORT}...")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except KeyboardInterrupt:
            print("\n[ENCERRADO] Servidor desligado.")
            break
        except Exception as e:
            print(f"[ERRO] Falha no servidor: {e}")

    server.close()

def posto_mais_proximo(posicao_cliente):
    """Retorna o nome do posto mais próximo baseado na posição."""
    menor_dist = float('inf')
    escolhido = None

    for nome_posto, posicao_posto in postos_de_recarga.items():
        dist = abs(posicao_cliente - posicao_posto)
        if dist < menor_dist:
            menor_dist = dist
            escolhido = nome_posto

    return escolhido

if __name__ == "__main__":
    main()

import socket
import threading

HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 5000        # Porta do servidor

def handle_client(conn, addr):
    """Lida com um cliente conectado."""
    print(f"[NOVA CONEXÃO] Conectado a {addr}")

    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            response = "Nenhum comando recebido!"
        elif data == "START":
            response = "Carregamento iniciado!"
        elif data == "STOP":
            response = "Carregamento encerrado!"
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

if __name__ == "__main__":
    main()

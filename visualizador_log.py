import time
import os

ARQUIVO_LOG = "log.txt"

def seguir_log(arquivo):
    print("🔎 Acompanhando o log do servidor...\n")
    try:
        with open(arquivo, "r") as f:
            # Vai pro final do arquivo
            f.seek(0, os.SEEK_END)
            while True:
                linha = f.readline()
                if not linha:
                    time.sleep(0.5)
                    continue
                print(linha.strip())
    except FileNotFoundError:
        print("❌ Arquivo de log não encontrado. O servidor já foi iniciado?")
    except KeyboardInterrupt:
        print("\n🛑 Visualização encerrada.")

if __name__ == "__main__":
    seguir_log(ARQUIVO_LOG)

# monitoramento.py - atualizado para salvar logs em log.txt com origem personalizada
from datetime import datetime
import os

ARQUIVO_LOG = os.getenv("LOG_PATH", "log.txt")


def logar_evento(evento: str, origem: str = "CHARGE-POINT"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{timestamp}] [{origem}] {evento}"
    print(log)
    try:
        with open(ARQUIVO_LOG, "a") as f:
            f.write(log + "\n")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar log em arquivo: {e}")

# services/monitoramento.py
from datetime import datetime

def logar_evento(evento: str):
    """Registra eventos da estação de carga com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[MONITORAMENTO] {timestamp} - {evento}")

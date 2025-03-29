# services/agendador.py
from datetime import datetime

def horario_permitido():
    """Verifica se o horário atual está dentro da janela permitida (ex: 8h às 22h)."""
    agora = datetime.now().hour
    return 8 <= agora <= 22

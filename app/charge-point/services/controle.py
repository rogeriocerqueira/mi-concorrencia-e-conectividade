# services/controle.py
from services.agendador import horario_permitido
from services.monitoramento import logar_evento

def aceitar_carregamento():
    """Decide se o carregamento deve iniciar."""
    if horario_permitido():
        logar_evento("Carregamento autorizado.")
        return True
    else:
        logar_evento("Carregamento negado - fora do horário permitido.")
        return False

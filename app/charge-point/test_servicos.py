# test_servicos.py
from services.agendador import horario_permitido
from services.monitoramento import logar_evento
from services.controle import aceitar_carregamento

print("Horário permitido?", horario_permitido())
logar_evento("Teste de evento manual")
print("Aceita carregar?", aceitar_carregamento())

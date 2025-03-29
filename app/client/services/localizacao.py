# client/services/localizacao.py
import random

# Começa o carro em uma posição aleatória entre 0 e 100
posicao_atual = random.randint(0, 100)

def atualizar_posicao():
    """Simula o movimento do carro em linha reta."""
    global posicao_atual
    movimento = random.choice([-3, -2, -1, 0, 1, 2, 3])  # pode andar pra frente, parar ou voltar
    posicao_atual += movimento
    posicao_atual = max(0, min(100, posicao_atual))  # limite entre 0 e 100
    return posicao_atual

def obter_posicao():
    """Retorna a posição atual do carro."""
    return posicao_atual

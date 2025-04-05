import time

def carregar_bateria(nivel_atual):
    print("[RECARGA] Iniciando recarga da bateria...")
    while nivel_atual < 100:
        time.sleep(30)  # Simula 30 segundos de carregamento
        nivel_atual = min(100, nivel_atual + 10)
        print(f"[RECARGA] Nível atual: {nivel_atual}%")

    print("[RECARGA] Bateria totalmente carregada!")
    return nivel_atual

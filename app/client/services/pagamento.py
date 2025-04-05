def processar_pagamento(id_cliente, energia_recarregada, preco_kwh=1.5):
    valor_total = energia_recarregada * preco_kwh
    print(f"[PAGAMENTO] Cliente: {id_cliente}")
    print(f"[PAGAMENTO] Energia recarregada: {energia_recarregada} kWh")
    print(f"[PAGAMENTO] Valor a pagar: R$ {valor_total:.2f}")
    print("[PAGAMENTO] Pagamento realizado com sucesso!")
    return valor_total

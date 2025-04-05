import os

ARQUIVO_CADASTRO = "cadastros.txt"

def ja_cadastrado(id_cliente):
    if not os.path.exists(ARQUIVO_CADASTRO):
        return False
    with open(ARQUIVO_CADASTRO, "r") as f:
        for linha in f:
            if linha.startswith(id_cliente + ","):
                return True
    return False

def cadastrar_cliente(id_cliente, posicao, nivel_bateria):
    if ja_cadastrado(id_cliente):
        print(f"[AVISO] Cliente '{id_cliente}' já está cadastrado.")
        return False

    linha = f"{id_cliente},{posicao},{nivel_bateria}\n"
    with open(ARQUIVO_CADASTRO, "a") as f:
        f.write(linha)
    print(f"[CADASTRO] Cliente '{id_cliente}' cadastrado com sucesso.")
    return True

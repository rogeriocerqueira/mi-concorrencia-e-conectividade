# 🔋 Sistema de Recarga de Veículos Elétricos

Este projeto simula a interação entre **veículos elétricos (clientes)**, **postos de recarga (charge-points)** e um **servidor central** que coordena a distribuição. A arquitetura é orientada a serviços e executada em contêiners Docker.

---

## 📌 Funcionalidades
- [x] Clientes simulam movimento e solicitam recarga
- [x] Servidor escolhe o charge-point mais próximo
- [x] Cada charge-point verifica se o horário é permitido para carregamento
- [x] Logs persistentes em `log.txt`
- [x] Visualização interativa via terminal com `rich`

---

## 🗂 Estrutura de Diretórios

```
mi-concorrencia-e-conectividade/
├── app/
│   ├── client/
│   │   ├── client.py
│   │   └── services/
│   │       ├── comunicacao.py
│   │       ├── localizacao.py
│   │       └── __init__.py
│   ├── server/
│   │   ├── server.py
│   │   └── log.txt
│   └── charge-point/
│       ├── charge.py
│       └── services/
│           ├── agendador.py
│           ├── controle.py
│           ├── monitoramento.py
│           └── __init__.py
├── .env
├── .gitignore
├── docker-compose.yml
├── painel_terminal.py
├── visualizador_log.py
```

---

## ▶️ Execução Passo a Passo

### 1. Subir os containers:
```bash
docker compose -p recarga up --build
```

### 2. Acessar o cliente:
```bash
docker exec -it recarga-client-1 bash
python3 client.py
```

### 3. Comandos do cliente:
```
POSICAO:<numero>    # ex: POSICAO:45
START               # solicita carregamento
STOP                # cancela carregamento
EXIT                # encerra cliente
```

### 4. Visualizar logs em tempo real:
```bash
python3 painel_terminal.py
```

Ou simplesmente:
```bash
tail -f app/server/log.txt
```

---

## 🧠 Arquitetura

Fluxo resumido:
- Cliente envia POSICAO
- Servidor escolhe posto mais próximo e envia START
- Posto inicia carregamento se estiver dentro do horário permitido
- Ao final, envia COMPLETE para o servidor
- Tudo é logado em `log.txt`

🔗 Diagrama da arquitetura:
[📄 Clique para ver o PDF do fluxograma](arquitetura_recarga.pdf)

---

## 📦 Requisitos
- Docker
- Docker Compose
- Python 3.8+ (fora do container)
- Biblioteca `rich`:
```bash
pip install rich
```

---

## ✨ Autor
Projeto criado por [Seu Nome Aqui].

Colabore, teste e aprimore!
import time
import os
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

ARQUIVO_LOG = "app/server/log.txt" if os.path.exists("app/server/log.txt") else "log.txt"

console = Console()
eventos_por_origem = defaultdict(list)

def carregar_logs():
    eventos_por_origem.clear()
    if not os.path.exists(ARQUIVO_LOG):
        return
    with open(ARQUIVO_LOG, "r") as f:
        for linha in f:
            if "] [" in linha:
                _, resto = linha.strip().split("] [", 1)
                origem, mensagem = resto.split("] ", 1)
                eventos_por_origem[origem].append(mensagem)

def construir_painel():
    tabelas = []
    for origem, eventos in eventos_por_origem.items():
        tabela = Table(show_header=True, header_style="bold cyan")
        tabela.add_column(origem, style="bold green")
        for ev in eventos[-5:]:  # últimos 5 eventos
            tabela.add_row(ev)
        tabelas.append(Panel(tabela, expand=True))
    return Panel.fit(Table.grid().add_row(*tabelas), title="🔋 Painel de Recarga - Terminal", border_style="bold yellow")

def painel_interativo():
    with Live(refresh_per_second=2, screen=True) as live:
        while True:
            carregar_logs()
            painel = construir_painel()
            live.update(painel)
            time.sleep(1)

if __name__ == "__main__":
    try:
        painel_interativo()
    except KeyboardInterrupt:
        console.print("\n🛑 Painel encerrado.", style="bold red")

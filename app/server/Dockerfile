# Usa a imagem oficial do Python 3.12.3
FROM python:3.12.3

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do servidor
COPY /server/ /app/

# Instala dependências (se necessário)
RUN pip install --no-cache-dir -r requirements.txt || true

# Expõe a porta do servidor
EXPOSE 5000

# Define o comando de execução
CMD ["python", "server.py"]

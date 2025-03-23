# Dockerfile
FROM python:3.12.3

WORKDIR /app

COPY server/server.py /app/server.py
COPY client/client.py /app/client.py

CMD ["python", "/app/server.py"]

#!/bin/bash

# Script para corrigir permissões dos diretórios Mosquitto
# Autor: Rogério Cerqueira

echo "Corrigindo permissões da pasta app/mosquitto/BA..."
sudo chown -R $USER:$USER app/mosquitto/BA
sudo chmod -R u+rw app/mosquitto/BA

echo "Corrigindo permissões da pasta app/mosquitto/MA..."
sudo chown -R $USER:$USER app/mosquitto/MA
sudo chmod -R u+rw app/mosquitto/MA

echo "Corrigindo permissões da pasta app/mosquitto/SE..."
sudo chown -R $USER:$USER app/mosquitto/SE
sudo chmod -R u+rw app/mosquitto/SE

echo "Corrigindo permissões da pasta mosquitto central..."
sudo chown -R $USER:$USER mosquitto
sudo chmod -R u+rw mosquitto

echo "Permissões corrigidas com sucesso! ✅"

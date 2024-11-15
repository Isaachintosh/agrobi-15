#!/bin/bash

# Atualizar o sistema
sudo apt-get update

# Remover versões antigas do Docker
# sudo apt-get remove docker docker-engine docker.io containerd runc

# Instalar pacotes para permitir o uso de repositórios HTTPS
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# automatizar
#   comandos git para configurar nickname e email de user github via input no terminal do usuário
#   geração / adição e ativação de chave ed25519 + cat da chave publica

# Adicionar a chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar o repositório estável do Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualizar novamente para obter as informações do novo repositório
sudo apt-get update

# Instalar o Docker Engine e o Docker CLI
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Adicionar o usuário atual ao grupo "docker" para executar comandos Docker sem sudo
sudo usermod -aG docker $USER

# Reiniciar o serviço Docker
sudo systemctl restart docker

echo "Docker foi reinstalado e configurado com sucesso!"
echo "Deu bom!"

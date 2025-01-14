# Use a imagem base mínima do Python
FROM python:3.11-slim

# Atualiza os repositórios e instala ferramentas do sistema
RUN apt-get update && apt-get install -y \
    unrar-free \
    p7zip-full \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho para o diretório src
WORKDIR /app

# Copia os arquivos de dependências para a raiz do diretório de trabalho atual
COPY src/requirements.txt .

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação para o diretório de trabalho
COPY ./src ./app

# Expor a porta que a aplicação utiliza
EXPOSE 8080

# Comando para executar a aplicação
CMD ["python3", "app.py"]

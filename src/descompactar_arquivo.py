import rarfile
import zipfile
import os
import shutil

def limpar_pasta(pasta):
    """
    Remove todos os arquivos e subdiretórios dentro da pasta especificada.

    Parâmetros:
        pasta (str): Caminho para a pasta que será limpa.
    """
    if os.path.exists(pasta):
        for item in os.listdir(pasta):
            item_path = os.path.join(pasta, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove arquivos ou links simbólicos
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove diretórios e conteúdo
    else:
        os.makedirs(pasta)  # Cria a pasta se ela não existir

def descompactar_arquivo(origem_arquivo, destino_extracao, pasta_temp):
    """
    Descompacta um arquivo ZIP ou RAR de um local de origem para um local de destino,
    limpando a pasta temporária antes de iniciar.

    Parâmetros:
        origem_arquivo (str): Caminho completo do arquivo de origem (ZIP ou RAR).
        destino_extracao (str): Diretório onde os arquivos serão extraídos.
        pasta_temp (str): Caminho para a pasta temporária que será limpa antes da extração.
    """
    # Limpar a pasta temporária
    limpar_pasta(pasta_temp)

    # Verificar a existência do arquivo de origem e criar o diretório de destino, se necessário
    if not os.path.exists(origem_arquivo):
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {origem_arquivo}")
    if not os.path.exists(destino_extracao):
        os.makedirs(destino_extracao)

    # Descompactar o arquivo
    if origem_arquivo.lower().endswith('.rar'):
        try:
            with rarfile.RarFile(origem_arquivo) as rar:
                rar.extractall(destino_extracao)
            print(f"Arquivo RAR extraído com sucesso em: {destino_extracao}")
        except rarfile.Error as e:
            raise RuntimeError(f"Erro ao descompactar o arquivo RAR: {e}")
    elif origem_arquivo.lower().endswith('.zip'):
        try:
            with zipfile.ZipFile(origem_arquivo, 'r') as zip_ref:
                zip_ref.extractall(destino_extracao)
            print(f"Arquivo ZIP extraído com sucesso em: {destino_extracao}")
        except zipfile.BadZipFile as e:
            raise RuntimeError(f"Erro ao descompactar o arquivo ZIP: {e}")
    else:
        raise ValueError("Formato de arquivo não suportado. Use arquivos .rar ou .zip.")

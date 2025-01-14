import pytest
from unittest.mock import patch
import subprocess
import os
import sys

# Permite importar o módulo etl_scripts.py corretamente
# Na linha abaixo, o caminho '../' é adicionado ao sys.path para que o Python possa encontrar o módulo etl_script.py
# O caminho '../' é necessário porque o arquivo de teste está dentro do diretório 'tests' e o módulo etl_script.py está no diretório raiz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import descompactar_arquivo

# Testes unitários
def test_arquivo_nao_encontrado():
    with patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = lambda x: False
        with pytest.raises(FileNotFoundError):
            descompactar_arquivo('caminho/invalido.rar', 'diretorio/destino')

def test_extracao_arquivo_rar_sucesso():
    with patch('os.path.exists') as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('subprocess.run') as mock_run:
        
        mock_exists.side_effect = lambda x: True
        descompactar_arquivo('arquivo.rar', 'diretorio/destino')
        mock_run.assert_called_once_with(['unrar', 'x', '-o+', 'arquivo.rar', 'diretorio/destino'], check=True)

def test_extracao_arquivo_zip_sucesso():
    with patch('os.path.exists') as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('subprocess.run') as mock_run:
        
        mock_exists.side_effect = lambda x: True
        descompactar_arquivo('arquivo.zip', 'diretorio/destino')
        mock_run.assert_called_once_with(['7z', 'x', '-aoa', 'arquivo.zip', '-odiretorio/destino'], check=True)

def test_formato_nao_suportado():
    with patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = lambda x: True
        with pytest.raises(ValueError):
            descompactar_arquivo('arquivo.txt', 'diretorio/destino')

def test_erro_execucao_comando():
    with patch('os.path.exists') as mock_exists, \
         patch('subprocess.run') as mock_run:
        
        mock_exists.side_effect = lambda x: True
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
        with pytest.raises(RuntimeError):
            descompactar_arquivo('arquivo.rar', 'diretorio/destino')
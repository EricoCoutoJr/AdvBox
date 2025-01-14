import pytest
import os
import pandas as pd
from unittest.mock import patch, mock_open
import sys

# Permite importar o módulo carregar.py corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import carregar_tabelas_csv


@patch('os.path.isdir')
def test_diretorio_nao_encontrado(mock_isdir):
    mock_isdir.return_value = False
    with pytest.raises(FileNotFoundError):
        carregar_tabelas_csv('diretorio/inexistente')

@patch('os.listdir')
@patch('os.path.isdir')
@patch('builtins.open', new_callable=mock_open, read_data='coluna1;coluna2\n1;2\n3;4')
@patch('pandas.read_csv')
def test_carregar_csv_sucesso(mock_read_csv, mock_open, mock_isdir, mock_listdir):
    mock_isdir.return_value = True
    mock_listdir.return_value = ['tabela.csv']
    mock_read_csv.return_value = pd.DataFrame({'coluna1': [1, 3], 'coluna2': [2, 4]})

    # Ajuste para o mock_open para leitura binária
    mock_open.return_value.read.return_value = b'coluna1;coluna2\n1;2\n3;4'
    
    tabelas = carregar_tabelas_csv('diretorio/extracao')
    assert 'tabela' in tabelas
    pd.testing.assert_frame_equal(tabelas['tabela'], pd.DataFrame({'coluna1': [1, 3], 'coluna2': [2, 4]}))

@patch('os.listdir')
@patch('os.path.isdir')
@patch('builtins.open', new_callable=mock_open, read_data='coluna1;coluna2\n1;2\n3;4')
def test_csv_sem_arquivos(mock_open, mock_isdir, mock_listdir):
    mock_isdir.return_value = True
    mock_listdir.return_value = []
    
    tabelas = carregar_tabelas_csv('diretorio/extracao')
    assert tabelas == {}

@patch('os.listdir')
@patch('os.path.isdir')
@patch('builtins.open', new_callable=mock_open)
def test_carregar_csv_sem_coluna(mock_open, mock_isdir, mock_listdir):
    mock_isdir.return_value = True
    mock_listdir.return_value = ['arquivo_vazio.csv']
    mock_open.return_value.read.return_value = b""
    
    with patch('pandas.read_csv', side_effect=pd.errors.EmptyDataError):
        tabelas = carregar_tabelas_csv('diretorio/extracao')
        assert tabelas == {}
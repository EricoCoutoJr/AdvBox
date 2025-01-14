import pytest
import pandas as pd
import os
from unittest.mock import patch
import sys

# Permite importar o módulo migrate.py corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import migrate_columns

def test_source_data_not_dataframe():
    with pytest.raises(ValueError, match="O parâmetro source_data deve ser um DataFrame."):
        migrate_columns("not_a_dataframe", "destination.xlsx", {"col1": "Column 1"})

@patch('os.path.exists', return_value=False)
def test_destination_file_not_found(mock_exists):
    source_data = pd.DataFrame({'col1': [1, 2]})
    with pytest.raises(FileNotFoundError, match="O arquivo de destino não foi encontrado: destination.xlsx"):
        migrate_columns(source_data, "destination.xlsx", {"col1": "Column 1"})

@patch('pandas.read_excel')
@patch('os.path.exists', return_value=True)
def test_column_mapping_error(mock_exists, mock_read_excel):
    source_data = pd.DataFrame({'col1': [1, 2]})
    mock_read_excel.return_value = pd.DataFrame()  # Retorna um DataFrame vazio para o destino

    with pytest.raises(ValueError, match="Erro ao mapear colunas"):
        migrate_columns(source_data, "destination.xlsx", {"not_a_col": "Column 1"})

@patch('pandas.read_excel')
@patch('os.path.exists', return_value=True)
def test_successful_migration(mock_exists, mock_read_excel):
    source_data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_excel.return_value = pd.DataFrame({'Column 1': [], 'Column 2': []})

    # Executa a migração
    result = migrate_columns(source_data, "destination.xlsx", {"col1": "Column 1", "col2": "Column 2"})

    # Ajusta os tipos de dados do resultado esperado para corresponder ao resultado real
    expected_result = pd.DataFrame({'Column 1': [1, 2], 'Column 2': [3, 4]}, dtype='float64')

    # Verifica a igualdade dos dataframes
    pd.testing.assert_frame_equal(result, expected_result)
import pytest
import sys, os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import padronizar_coluna

def test_padronizar_coluna_sucesso():
    df = pd.DataFrame({'categoria': ['A', 'B', 'C', 'A', 'C']})
    mapping_dict = {'A': 'Alpha', 'B': 'Beta', 'C': 'Gamma'}

    expected_df = pd.DataFrame({'categoria': ['Alpha', 'Beta', 'Gamma', 'Alpha', 'Gamma']})
    result_df = padronizar_coluna(df, 'categoria', mapping_dict)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_valores_nao_mapeados():
    df = pd.DataFrame({'categoria': ['A', 'B', 'D', 'A', 'E']})
    mapping_dict = {'A': 'Alpha', 'B': 'Beta'}

    expected_df = pd.DataFrame({'categoria': ['Alpha', 'Beta', 'D', 'Alpha', 'E']})
    result_df = padronizar_coluna(df, 'categoria', mapping_dict)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_coluna_nao_existente():
    df = pd.DataFrame({'categoria': ['A', 'B', 'C']})
    mapping_dict = {'A': 'Alpha', 'B': 'Beta', 'C': 'Gamma'}

    with pytest.raises(ValueError, match="A coluna 'nonexistent' não existe no DataFrame."):
        padronizar_coluna(df, 'nonexistent', mapping_dict)

def test_coluna_vazia():
    df = pd.DataFrame({'categoria': []})
    mapping_dict = {'A': 'Alpha', 'B': 'Beta', 'C': 'Gamma'}

    expected_df = pd.DataFrame({'categoria': []})
    result_df = padronizar_coluna(df, 'categoria', mapping_dict)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_dataframe_vazio():
    df = pd.DataFrame({'categoria': []})
    mapping_dict = {'A': 'Alpha', 'B': 'Beta', 'C': 'Gamma'}

    expected_df = pd.DataFrame({'categoria': []})
    result_df = padronizar_coluna(df, 'categoria', mapping_dict)

    pd.testing.assert_frame_equal(result_df, expected_df)
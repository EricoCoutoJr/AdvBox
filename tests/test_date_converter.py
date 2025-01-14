import pytest
import pandas as pd
import sys
import os

# Permite importar o módulo date_converter.py corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import converter_datas


def test_successful_conversion_single_format():
    df = pd.DataFrame({'date': ['2025-01-01', '2025-02-01', '2025-03-01']})
    formatos_entrada = ['%Y-%m-%d']
    formato_saida = '%d/%m/%Y'

    expected_df = pd.DataFrame({'date': ['01/01/2025', '01/02/2025', '01/03/2025']})
    result_df = converter_datas(df, formatos_entrada, formato_saida)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_successful_conversion_multiple_formats():
    df = pd.DataFrame({'date': ['01-01-2025', '2025/02/01', 'March 1, 2025']})
    formatos_entrada = ['%d-%m-%Y', '%Y/%m/%d', '%B %d, %Y']
    formato_saida = '%Y-%m-%d'

    expected_df = pd.DataFrame({'date': ['2025-01-01', '2025-02-01', '2025-03-01']})
    result_df = converter_datas(df, formatos_entrada, formato_saida)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_no_conversion_on_invalid_format():
    df = pd.DataFrame({'date': ['2025-31-01', 'invalid-date', '03-01-2025']})
    formatos_entrada = ['%Y-%m-%d']
    formato_saida = '%d/%m/%Y'

    expected_df = pd.DataFrame({'date': ['2025-31-01', 'invalid-date', '03-01-2025']})
    result_df = converter_datas(df, formatos_entrada, formato_saida)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_partial_conversion_with_valid_and_invalid_dates():
    df = pd.DataFrame({'date': ['2025-01-01', 'invalid-date', '2025-03-01']})
    formatos_entrada = ['%Y-%m-%d']
    formato_saida = '%d/%m/%Y'

    expected_df = pd.DataFrame({'date': ['01/01/2025', 'invalid-date', '01/03/2025']})
    result_df = converter_datas(df, formatos_entrada, formato_saida)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_no_conversion_for_non_string_columns():
    df = pd.DataFrame({'date': [20250101, 20250201, 20250301]})
    formatos_entrada = ['%Y-%m-%d']
    formato_saida = '%d/%m/%Y'

    expected_df = pd.DataFrame({'date': [20250101, 20250201, 20250301]})
    result_df = converter_datas(df, formatos_entrada, formato_saida)

    pd.testing.assert_frame_equal(result_df, expected_df)
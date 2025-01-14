import sys, os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import converter_texto_para_maiusculas

def test_converter_texto_para_maiusculas_sucesso():
    df = pd.DataFrame({
        'texto': ['abc', 'def', 'ghi'],
        'numero': [1, 2, 3]
    })
    expected_df = pd.DataFrame({
        'texto': ['ABC', 'DEF', 'GHI'],
        'numero': [1, 2, 3]
    })
    result_df = converter_texto_para_maiusculas(df)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_converter_colunas_mistas():
    df = pd.DataFrame({
        'texto': ['abc', 'def', 'ghi'],
        'numero': [1, 2, 3],
        'data': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01']),
        'mixed': ['xyz', 123, 'uvw']
    })
    expected_df = pd.DataFrame({
        'texto': ['ABC', 'DEF', 'GHI'],
        'numero': [1, 2, 3],
        'data': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01']),
        'mixed': ['XYZ', 123, 'UVW']
    })
    result_df = converter_texto_para_maiusculas(df)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_converter_series():
    series = pd.Series(['abc', 'def', 'ghi'])
    expected_series = pd.Series(['ABC', 'DEF', 'GHI'], name=series.name)
    result_series = converter_texto_para_maiusculas(series)

    pd.testing.assert_series_equal(result_series.squeeze(), expected_series, check_names=False)

def test_dataframe_vazio():
    df = pd.DataFrame(columns=['texto', 'numero'])
    expected_df = pd.DataFrame(columns=['texto', 'numero'])
    result_df = converter_texto_para_maiusculas(df)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_coluna_vazia():
    df = pd.DataFrame({'texto': [], 'numero': []})
    expected_df = pd.DataFrame({'texto': [], 'numero': []})
    result_df = converter_texto_para_maiusculas(df)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_sem_colunas_de_texto():
    df = pd.DataFrame({
        'numero': [1, 2, 3],
        'data': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01'])
    })
    expected_df = df.copy()
    result_df = converter_texto_para_maiusculas(df)

    pd.testing.assert_frame_equal(result_df, expected_df)

import sys, os
import pandas as pd
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from etl_script import criar_e_salvar_dataframe_vazio

def test_criar_e_salvar_dataframe_vazio():
    colunas = ['coluna1', 'coluna2', 'coluna3']
    caminho_destino = '/caminho/falso/para/não/salvar.xlsx'

    # Usar patch para simular o método to_excel e evitar a escrita real
    with patch('pandas.DataFrame.to_excel') as mock_to_excel:
        df = criar_e_salvar_dataframe_vazio(colunas, caminho_destino)
        
        # Verifica se o DataFrame foi criado com as colunas corretas e está vazio
        expected_df = pd.DataFrame(columns=colunas)
        pd.testing.assert_frame_equal(df, expected_df)

        # Verifica se o método to_excel foi chamado com os argumentos corretos
        mock_to_excel.assert_called_once_with(caminho_destino, index=False)

        # Verifica se a mensagem de salvamento foi impressa corretamente
        with patch('builtins.print') as mock_print:
            criar_e_salvar_dataframe_vazio(colunas, caminho_destino)
            mock_print.assert_called_with(f"DataFrame salvo em: {caminho_destino}")

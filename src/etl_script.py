import os
import pandas as pd
import subprocess
import chardet

def descompactar_arquivo(origem_arquivo, destino_extracao):
    """
    Descompacta um arquivo ZIP ou RAR para o diretório especificado.

    Parâmetros:
        caminho_arquivo (str): O caminho completo do arquivo a ser descompactado.
        diretorio_extracao (str): O diretório onde os arquivos serão extraídos.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        ValueError: Formato de arquivo não suportado. Use arquivos .rar ou .zip.
        RuntimeError: Erro ao executar o comando de descompactação.
    """
    if not os.path.exists(origem_arquivo):
        raise FileNotFoundError(f"Arquivo de origem não encontrado: {origem_arquivo}")
    if not os.path.exists(destino_extracao):
        os.makedirs(destino_extracao, exist_ok=True, mode=0o777)


    try:
        if origem_arquivo.lower().endswith('.rar'):
            # Adiciona o flag "-o+" para sobrescrever arquivos existentes
            subprocess.run(['unrar', 'x', '-o+', origem_arquivo, destino_extracao], check=True)
        elif origem_arquivo.lower().endswith('.zip'):
            # Adiciona a opção "-aoa" para sobrescrever arquivos existentes
            subprocess.run(['7z', 'x', '-aoa', origem_arquivo, '-o' + destino_extracao], check=True)
        else:
            raise ValueError("Formato de arquivo não suportado. Use arquivos .rar ou .zip.")
        print(f"Arquivo extraído com sucesso em: {destino_extracao}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao executar o comando de descompactação: {e}")

def carregar_tabelas_csv(diretorio_extracao):
    """
    Carrega todas as tabelas em arquivos CSV do diretório especificado.

    Parâmetros:
    diretorio_extracao (str): Caminho para o diretório contendo os arquivos CSV extraídos.

    Retorna:
    dict: Dicionário com nomes dos arquivos (sem extensão) como chaves e DataFrames como valores.
    """
    if not os.path.isdir(diretorio_extracao):
        raise FileNotFoundError(f"O diretório {diretorio_extracao} não foi encontrado.")

    arquivos = os.listdir(diretorio_extracao)
    arquivos_csv = [arq for arq in arquivos if arq.lower().endswith('.csv')]
    tabelas = {}

    for arquivo in arquivos_csv:
        caminho_arquivo = os.path.join(diretorio_extracao, arquivo)
        nome_tabela = os.path.splitext(arquivo)[0]

        try:
            # Detecta a codificação do arquivo
            with open(caminho_arquivo, 'rb') as f:
                resultado = chardet.detect(f.read(10000))
                encoding = resultado['encoding']

            # Tenta ler o arquivo CSV com o delimitador ';'
            try:
                with open(caminho_arquivo, 'r', encoding=encoding) as f:
                    df = pd.read_csv(f, sep=';', engine='python', on_bad_lines='skip')
            except pd.errors.ParserError:
                # Se falhar, tenta ler com o delimitador padrão ','
                with open(caminho_arquivo, 'r', encoding=encoding) as f:
                    df = pd.read_csv(f, sep=',', engine='python', on_bad_lines='skip')

            tabelas[nome_tabela] = df
            print(f"Tabela '{nome_tabela}' carregada com sucesso.")

        except Exception as e:
            print(f"Erro ao carregar '{arquivo}': {e}")

    return tabelas

def migrate_columns(source_data, destination_file_path, column_mapping):
    """
    Migra colunas de um DataFrame de origem para um arquivo Excel de destino, renomeando-as conforme especificado.

    Parâmetros:
        source_data (pd.DataFrame): DataFrame de origem com os dados a serem migrados.
        destination_file_path (str): Caminho para o arquivo de destino (Excel).
        column_mapping (dict): Dicionário que mapeia as colunas do DataFrame de origem para as colunas do DataFrame de destino.

    Retorno:
        pd.DataFrame: DataFrame atualizado com os dados migrados.
    """
    if not isinstance(source_data, pd.DataFrame):
        raise ValueError("O parâmetro source_data deve ser um DataFrame.")

    if not os.path.exists(destination_file_path):
        raise FileNotFoundError(f"O arquivo de destino não foi encontrado: {destination_file_path}")

    # Carregar o arquivo de destino diretamente com pandas
    destination_data = pd.read_excel(destination_file_path)

    # Mapear e renomear as colunas do DataFrame de origem
    try:
        mapped_data = source_data[list(column_mapping.keys())].rename(columns=column_mapping)
    except KeyError as e:
        raise ValueError(f"Erro ao mapear colunas: {e}")

    # Combinar os dados mapeados com o DataFrame de destino
    updated_destination_data = pd.concat([destination_data, mapped_data], ignore_index=True)

    return updated_destination_data

def converter_datas(df, formatos_entrada, formato_saida):
    """
    Converte colunas de string que representam datas de múltiplos formatos para um formato especificado.

    Parâmetros:
        df (pandas.DataFrame): DataFrame a ser processado.
        formatos_entrada (list): Lista de strings representando os formatos de data de entrada.
        formato_saida (str): String representando o formato de data desejado.

    Retorna:
        pandas.DataFrame: DataFrame com as colunas de data convertidas para o formato especificado.
    """
    for coluna in df.columns:
        if df[coluna].dtype == 'object':  # Verifica se a coluna é do tipo string
            for i in df.index:
                data_original = df.at[i, coluna]
                convertida = False  # Flag para indicar se a conversão foi bem-sucedida
                for formato in formatos_entrada:
                    try:
                        # Tenta converter a data usando o formato atual
                        data_convertida = pd.to_datetime(data_original, format=formato, errors='raise')
                        df.at[i, coluna] = data_convertida.strftime(formato_saida)
                        convertida = True
                        break  # Sai do loop se a conversão for bem-sucedida
                    except (ValueError, TypeError):
                        continue  # Tenta o próximo formato se a conversão falhar
                if not convertida:
                    # Restaura a data original se a conversão falhar em todos os formatos
                    df.at[i, coluna] = data_original
    return df

def padronizar_coluna(dataframe, coluna, mapping_dict):
    """
    Padroniza os valores de uma coluna em um DataFrame com base em um dicionário de mapeamento.

    Parâmetros:
        dataframe (pd.DataFrame): O DataFrame a ser modificado.
        coluna (str): O nome da coluna que será padronizada.
        mapping_dict (dict): Um dicionário contendo os valores originais como chaves e os valores padronizados como valores.

    Retorno:
        pd.DataFrame: DataFrame com a coluna padronizada.
    """
    # Verificar se a coluna existe no DataFrame
    if coluna not in dataframe.columns:
        raise ValueError(f"A coluna '{coluna}' não existe no DataFrame.")

    # Aplicar a padronização usando o dicionário de mapeamento
    dataframe[coluna] = dataframe[coluna].replace(mapping_dict)

    # Inferir objetos explicitamente para evitar o comportamento de downcasting
    dataframe[coluna] = dataframe[coluna].infer_objects(copy=False)

    return dataframe

def converter_texto_para_maiusculas(df):
    """
    Converte o conteúdo das colunas de texto para maiúsculas, mantendo inalteradas as colunas numéricas ou de datas.

    Parâmetros:
    df (pandas.DataFrame): DataFrame a ser processado.

    Retorna:
    pandas.DataFrame: DataFrame com colunas de texto em maiúsculas.
    """
    # Caso o input seja uma Series, convertê-la para um DataFrame
    if isinstance(df, pd.Series):
        df = df.to_frame()

    for coluna in df.columns:
        if df[coluna].dtype == 'object':
            df[coluna] = df[coluna].apply(lambda x: x.upper() if isinstance(x, str) else x)
    return df

def criar_e_salvar_dataframe_vazio(colunas, caminho_destino):
    """
    Cria um DataFrame vazio com as colunas especificadas e o salva em formato XLSX no local de destino.

    Parâmetros:
        colunas (list): Lista de nomes de colunas.
        caminho_destino (str): Caminho completo do arquivo XLSX onde o DataFrame será salvo.

    Retorna:
        pd.DataFrame: DataFrame vazio criado.
    """
    # Cria o DataFrame vazio
    df = pd.DataFrame(columns=colunas)
    
    # Salva o DataFrame em formato XLSX
    try:
        df.to_excel(caminho_destino, index=False)
    except Exception as e:
        print(f"Erro ao salvar os arquivos: {e}")
    
    print(f"DataFrame salvo em: {caminho_destino}")
    return df

def executar_etl(arquivo_compactado, pasta_saida):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp_folder = os.path.join(BASE_DIR, 'temp')
    #os.makedirs(temp_folder, exist_ok=True)

    # Descompactando (extraindo) o arquivo (Extract - ELT)
    descompactar_arquivo(arquivo_compactado, temp_folder)

    # Extraindo os dados das tabelas .csv para processamento (Estract - ELT)
    tabelas = carregar_tabelas_csv(temp_folder)

    # Criar os arquivos de saída - Clienetes e Processos (Load - ELT)
    saida1 = os.path.normpath(os.path.join(pasta_saida, 'clientes.xlsx'))
    saida2 = os.path.normpath(os.path.join(pasta_saida, 'processos.xlsx'))

    colunas_clientes = ['NOME', 'CPF CNPJ', 'RG', 'NACIONALIDADE', 'DATA DE NASCIMENTO',
       'ESTADO CIVIL', 'PROFISSÃO', 'SEXO', 'CELULAR', 'TELEFONE', 'EMAIL',
       'PAIS', 'ESTADO', 'CIDADE', 'BAIRRO', 'ENDEREÇO', 'CEP', 'PIS PASEP',
       'CTPS', 'CID', 'NOME DA MÃE', 'ORIGEM DO CLIENTE', 'ANOTAÇÕES GERAIS']
    clientes = criar_e_salvar_dataframe_vazio (colunas_clientes, saida1)

    colunas_processo = ['NOME DO CLIENTE', 'PARTE CONTRÁRIA', 'TIPO DE AÇÃO', 'GRUPO DE AÇÃO',
       'FASE PROCESSUAL', 'NÚMERO DO PROCESSO', 'PROCESSO ORIGINÁRIO',
       'TRIBUNAL', 'VARA', 'COMARCA', 'PROTOCOLO',
       'EXPECTATIVA/VALOR DA CAUSA', 'VALOR HONORÁRIOS', 'PASTA',
       'DATA CADASTRO', 'DATA FECHAMENTO', 'DATA TRANSITO',
       'DATA ARQUIVAMENTO', 'DATA REQUERIMENTO', 'RESPONSÁVEL',
       'ANOTAÇÕES GERAIS']
    processos = criar_e_salvar_dataframe_vazio (colunas_processo, saida2)

    # clientes.to_excel(saida1, index=False)
    # processos.to_excel(saida2, index=False)

    # Carregando os dados nas tabelas de saída - Clientes e Processos (Load - ELT)
    # Definição das colunas do dataframe de processos a serem migradas.
    processo_column_mapping = {
                                    'codarea_acao': 'TIPO DE AÇÃO',
                                    'numero_processo': 'NÚMERO DO PROCESSO',
                                    'data_distribuicao': 'DATA CADASTRO',
                                    'local_tramite': 'TRIBUNAL',
                                }
    # Definição das colunas do dataframe de clientes a serem migradas.
    clientes_column_mapping = {}
    print("Definição das colunas do dataframe de processos a serem migradas.")

    # Processo inicial de migração dos dados (dados não associados às outras tabelas)
    processos = migrate_columns(tabelas['v_processos_CodEmpresa_92577'],
                                saida2,
                                column_mapping=processo_column_mapping)
    clientes = migrate_columns(tabelas['v_clientes_CodEmpresa_92577'],
                               saida1,
                               column_mapping=clientes_column_mapping)
    print("Processo inicial de migração dos dados (dados não associados às outras tabelas).")

    # Tratamento das datas nos arquivos de processos e clientes
    formatos_entrada = ['%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S','%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']
    formato_saida = '%d/%m/%Y'
    processos = converter_datas(processos, formatos_entrada, formato_saida)
    clientes = converter_datas(clientes, formatos_entrada, formato_saida)
    print("Tratamento das datas nos arquivos de processos e clientes.")

    # Tratamento de coluna cidade
    cidade_mapping = {
                     'Floripa': 'Florianópolis',
                     'Florianopolis': 'Florianópolis',
                     'Rib. Do Pinhal': 'Ribeirão do Pinhal',
                     'Ribeirao do Pinhal': 'Ribeirão do Pinhal',
                     'Ribei. Pinhal': 'Ribeirão do Pinhal'
                     }
    clientes = padronizar_coluna(clientes, 'CIDADE', cidade_mapping)

    # Tratamento das strings para formato MAÚSCULO
    clientes = converter_texto_para_maiusculas(clientes)
    processos = converter_texto_para_maiusculas(processos)

    # Tratamento dos dados já carregados (ELT - Transform)
    clientes.to_excel(saida1, index=False)
    processos.to_excel(saida2, index=False)

    return 'clientes.xlsx', 'processos.xlsx'

from validate_docbr import CPF, CNPJ

cpf_validator = CPF()
cnpj_validator = CNPJ()

def remover_caracteres_nao_numericos(valor):
    """
    Remove caracteres não numéricos de uma string.
    """
    return re.sub(r'\D', '', valor)

def validar_e_formatar_cpf_cnpj(valor):
    """
    Valida e formata CPF ou CNPJ.
    Retorna o valor formatado se válido; caso contrário, retorna None.
    """
    valor = remover_caracteres_nao_numericos(valor)
    if len(valor) == 11 and cpf_validator.validate(valor):
        return cpf_validator.mask(valor)
    elif len(valor) == 14 and cnpj_validator.validate(valor):
        return cnpj_validator.mask(valor)
    else:
        return None

def processar_colunas_CPF_CNPJ(df, colunas):
    """
    Processa as colunas especificadas do DataFrame:
    - Remove caracteres não numéricos
    - Valida e formata CPF/CNPJ
    - Preenche com zeros à esquerda para atingir 11 (CPF) ou 14 (CNPJ) dígitos
    - Os CPF/CNPJ sairão com a mascara de seus respectivos formatos.

    Parâmetros:
    df (pandas.DataFrame): DataFrame a ser processado.
    colunas (list): Lista de nomes de colunas a serem processadas.
    """
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).apply(remover_caracteres_nao_numericos)
            df[coluna] = df[coluna].apply(lambda x: x.zfill(11) if len(x) <= 11 else x.zfill(14))
            df[coluna] = df[coluna].apply(validar_e_formatar_cpf_cnpj)
    return df

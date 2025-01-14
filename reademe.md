# Data ELT

Este projeto é responsável por extrair, carregar e  transformar dados existente em arquivos ZIP e RAR específico.
A decisão de usar o processo ELT ao invés de ETL, foi tomada em função da quantidade de dados a serem tratados antes do carregamento. Tratar os dados após o carregamento seria mais rápido e menor uso de recursos.  

## Estrutura do Projeto

  -  `src/`: Contém o código fonte.
<img src="https://pypi-camo.freetls.fastly.net/705545a847e60d6d4478c76a8146b9000e339c1c/68747470733a2f2f70616e6461732e7079646174612e6f72672f7374617469632f696d672f70616e6461732e737667" alt="Pandas Logo" width="200" height="100"> <img src="https://flask.palletsprojects.com/en/stable/_images/flask-horizontal.png" alt="Flask Logo" width="300" height="95">

-  `tests/`: Contém os arquivos de teste.
<img src="https://pypi-camo.freetls.fastly.net/1599e7e4caeaac6ca1a8d4ace3cefa8a0d160925/68747470733a2f2f6769746875622e636f6d2f7079746573742d6465762f7079746573742f7261772f6d61696e2f646f632f656e2f696d672f7079746573745f6c6f676f5f6375727665732e737667" alt="Logo do Pytest" width="200" height="100">


## Executando Testes

  

Para executar testes localmente:

  

```bash
python  -m  unittest  discover  -s  tests
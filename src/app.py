from flask import Flask, request, send_file, render_template
import os

from etl_script import executar_etl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
print(UPLOAD_FOLDER)
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
print(OUTPUT_FOLDER)

app = Flask(__name__, template_folder = os.path.join(BASE_DIR, 'templates'))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arquivo = request.files['file']
        if arquivo:
            caminho_arquivo = os.path.join(UPLOAD_FOLDER, arquivo.filename)
            arquivo.save(caminho_arquivo)
            
            # Executa o ETL
            saida1, saida2 = executar_etl(caminho_arquivo, OUTPUT_FOLDER)
            
            # Retorna os arquivos processados para download
            return render_template('index.html', download1=saida1, download2=saida2)
    
    return render_template('index.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    
    # Verifique se o arquivo existe antes de tentar fazer o download
    if not os.path.exists(file_path):
        return "Arquivo não encontrado.", 404
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
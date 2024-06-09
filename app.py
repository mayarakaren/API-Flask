from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import io
from contextlib import redirect_stdout
from models.knn import knn
from models.algGenetico import run_genetic_algorithm
from models.arvore import arvore
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

IMG_FOLDER = 'imagens'
BASES_FOLDER = 'bases'
os.makedirs(BASES_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo encontrado na requisição"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    try:
        # Garantir que o nome do arquivo é seguro para salvar no servidor
        filename = secure_filename(file.filename)

        # Salvar o arquivo no diretório apropriado
        file.save(os.path.join(BASES_FOLDER, filename))

        return jsonify({"file_path": os.path.join(BASES_FOLDER, filename)}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao salvar o arquivo: {str(e)}"}), 400

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()

    if 'filePath' not in data or 'algorithm' not in data:
        return jsonify({"erro": "Dados ausentes na requisição"}), 400

    file_path = data['filePath']
    algorithm = data['algorithm']
    image_path = ""
    output = ""
    accuracy = ""

    if algorithm == 'knn':
        f = io.StringIO()
        with redirect_stdout(f):
            output = knn(file_path)
        output = f.getvalue()
    elif algorithm == 'algGenetico':  # Ensure the correct name is used
        f = io.StringIO()
        with redirect_stdout(f):
            best_individual, image_path = run_genetic_algorithm(IMG_FOLDER)
        output = f.getvalue()
    elif algorithm == 'arvore':
        f = io.StringIO()
        with redirect_stdout(f):
            accuracy, image_path = arvore(file_path, IMG_FOLDER)
        output = f.getvalue()
    else:
        return jsonify({"erro": "Algoritmo inválido"}), 400

    response = {"output": output, "acurácia": accuracy if algorithm != 'algGenetico' else "N/A"}
    if image_path:
        response["imagem"] = f"/imagens/{os.path.basename(image_path)}"

    return jsonify(response), 200

@app.route('/imagens/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMG_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

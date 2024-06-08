from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import mimetypes
import os
import io
from contextlib import redirect_stdout
from models.knn import knn
from models.algGenetico import run_genetic_algorithm
from models.arvore import arvore

app = Flask(__name__)
CORS(app)

IMG_FOLDER = 'imagens'
os.makedirs(IMG_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo encontrado na requisição"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    try:
        # Detect file type and read accordingly
        content_type = mimetypes.guess_type(file.filename)[0]
        if file.filename.endswith('.data'):
            csv_data = pd.read_csv(file)
        else:
            csv_data = pd.read_csv(file, delimiter='\s+', header=None)
        file_path = os.path.join(IMG_FOLDER, file.filename)
        csv_data.to_csv(file_path, index=False)
    except Exception as e:
        return jsonify({"erro": f"Erro ao ler o arquivo: {str(e)}"}), 400

    return jsonify({"file_path": file_path}), 200

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

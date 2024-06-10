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

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()

    if 'algorithm' not in data:
        return jsonify({"erro": "Algoritmo não especificado"}), 400

    algorithm = data['algorithm']
    output = ""
    accuracy = None
    image_path = None

    try:
        if algorithm == 'knn':
            output = knn()
        elif algorithm == 'algGenetico':
            best_individual, image_path = run_genetic_algorithm(IMG_FOLDER)
            output = (
                    "======================================\n"
                    "O melhor indivíduo:\n"
                    f"X = {best_individual[0]}\n"
                    f"Y = {best_individual[1]}\n"
                    f"Fitness = {best_individual[2]}\n\n"
                )
        elif algorithm == 'arvore':
            if 'filePath' not in data:
                return jsonify({"erro": "Caminho do arquivo não especificado"}), 400
            file_path = data['filePath']
            accuracy, image_path = arvore(file_path, IMG_FOLDER)
            output = f"Acurácia do algoritmo de árvore de decisão: {accuracy * 100:.2f}" if accuracy is not None else "Erro ao executar o algoritmo"
        else:
            return jsonify({"erro": "Algoritmo inválido"}), 400

        response = {
            "output": output,
            "acurácia": accuracy if accuracy is not None else "N/A"
        }
        if image_path:
            response["imagem"] = f"/imagens/{os.path.basename(image_path)}"

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao executar o algoritmo: {str(e)}"}), 500


@app.route('/imagens/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMG_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

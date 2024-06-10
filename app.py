from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
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
            result = knn()
            output = (
                f"Quantidade de exemplos: {result['quantidade_exemplos']}\n"
                f"Quantidade de classes: {result['quantidade_classes']}\n"
                f"Quantidade de atributos: {result['quantidade_atributos']}\n"
                f"Taxa de acerto: {result['taxa_acerto']:.2f}%\n"
                f"----------------------------------\n"
                f"Saída do KNN:\n{result['output']}"
            )
        elif algorithm == 'algGenetico':
            best_individual, image_path, funcao_objetivo, dominio = run_genetic_algorithm(IMG_FOLDER)
            output = (
                "======================================\n"
                "O melhor indivíduo:\n"
                f"X = {best_individual[0]}\n"
                f"Y = {best_individual[1]}\n"
                f"Fitness = {best_individual[2]}\n\n"
                f"Função objetivo: {funcao_objetivo}\n"
                f"Domínio: {dominio}"
            )
        elif algorithm == 'arvore':
            if 'filePath' not in data:
                return jsonify({"erro": "Caminho do arquivo não especificado"}), 400
            file_path = data['filePath']
            result = arvore(file_path, IMG_FOLDER)
            accuracy = result['taxa_acerto']
            image_path = result['image_path']
            output = (
                f"Quantidade de exemplos: {result['quantidade_exemplos']}\n"
                f"Quantidade de classes: {result['quantidade_classes']}\n"
                f"Quantidade de atributos: {result['quantidade_atributos']}\n"
                f"Taxa de acerto: {result['taxa_acerto']:.2f}%\n"
                f"Modelo criado: {result['modelo_criado']}"
            )
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

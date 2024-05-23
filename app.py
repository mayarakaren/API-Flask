from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from models.knn import knn
from models.algGenetico import run_genetic_algorithm
from models.arvore import arvore

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo encontrado na requisição"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    try:
        csv_data = pd.read_csv(file)
    except Exception as e:
        return jsonify({"erro": f"Erro ao ler o arquivo CSV: {str(e)}"}), 400

    return csv_data.to_json(orient='records'), 200

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()

    if 'csvData' not in data or 'algorithm' not in data:
        return jsonify({"erro": "Dados ausentes na requisição"}), 400

    try:
        csv_data = pd.DataFrame(data['csvData'])
    except Exception as e:
        return jsonify({"erro": f"Erro ao converter dados para DataFrame: {str(e)}"}), 400

    algorithm = data['algorithm']
    image_path = ""

    if algorithm == 'knn':
        accuracy = knn(csv_data)
    elif algorithm == 'algGenetico':
        best_individual, image_path = run_genetic_algorithm()
        accuracy = "N/A"
    elif algorithm == 'arvore':
        accuracy, image_path = arvore()
    else:
        return jsonify({"erro": "Algoritmo inválido"}), 400

    response = {"acurácia": accuracy}
    if image_path:
        response["imagem"] = image_path

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)

# Documentação da API Flask

## Introdução

Esta API oferece funcionalidades para classificação de dados usando diferentes algoritmos de aprendizado de máquina. Atualmente, suporta os seguintes algoritmos:

- KNN (K-Nearest Neighbors)
- Algoritmo Genético
- Árvore de Decisão

## Executando o Projeto

Para executar o projeto, siga os passos abaixo:

1. Clone o repositório do GitHub para o seu ambiente local:

   ```bash
   git clone https://github.com/mayarakaren/API-Flask.git
   ```

2. Navegue até o diretório do projeto e instale as dependências necessárias:

   ```bash
   cd API-Flask
   pip install -r requirements.txt
   ```

3. Execute o servidor Flask para iniciar a API:

   ```bash
   python app.py
   ```

   O servidor será iniciado em http://localhost:5000/.

## Base URL

A base URL da API é:

```
http://localhost:5000/
```

## Métodos da API

### 1. Classificação

- **Endpoint:** /classify
- **Método:** POST

#### Parâmetros de Requisição:

| Parâmetro  | Tipo    | Descrição                                             |
|------------|---------|-------------------------------------------------------|
| algorithm  | string  | O algoritmo a ser utilizado (knn, algGenetico, arvore)|
| filePath   | string  | (Somente para algoritmo 'arvore') Caminho do arquivo contendo os dados (opcional)|

#### Corpo da Requisição:

```json
{
    "algorithm": "knn"
}
```

#### Resposta de Sucesso:

```json
{
    "output": "Resultado da classificação",
    "acurácia": "Valor da acurácia (N/A se não aplicável)",
    "imagem": "URL para a imagem de saída (se aplicável)"
}
```

#### Resposta de Erro:

```json
{
    "erro": "Descrição do erro"
}
```

### 2. Servir Imagem

- **Endpoint:** /imagens/<path:filename>
- **Método:** GET

#### Parâmetros de Requisição:

| Parâmetro  | Tipo    | Descrição                     |
|------------|---------|-------------------------------|
| filename   | string  | Nome do arquivo de imagem      |

## Código Fonte da API

1. **Importações e Configurações Iniciais**:
   ```python
   from flask import Flask, request, jsonify, send_from_directory
   from flask_cors import CORS
   import os
   from models.knn import knn
   from models.algGenetico import run_genetic_algorithm
   from models.arvore import arvore
   from werkzeug.utils import secure_filename
   ```

   - Aqui, são importadas as bibliotecas necessárias para criar a API Flask, gerenciar as rotas, lidar com solicitações HTTP, lidar com arquivos, etc. A função `CORS` é usada para permitir solicitações de origens diferentes (Cross-Origin Resource Sharing).
   
2. **Configuração das Pastas e Arquivos**:
   ```python
   app = Flask(__name__)
   CORS(app)

   IMG_FOLDER = 'imagens'
   BASES_FOLDER = 'bases'
   os.makedirs(BASES_FOLDER, exist_ok=True)
   os.makedirs(IMG_FOLDER, exist_ok=True)
   ```
   
   - Aqui, é criada uma instância da aplicação Flask e configurado o tratamento de CORS. As pastas `imagens` e `bases` são criadas (se não existirem) para armazenar imagens e dados de bases respectivamente.

3. **Endpoint para Classificação**:
   ```python
   @app.route('/classify', methods=['POST'])
   def classify():
       data = request.get_json()

       if 'algorithm' not in data:
           return jsonify({"erro": "Algoritmo não especificado"}), 400
       
       # Lógica para selecionar o algoritmo e executar a classificação
   ```

   - Este trecho define um endpoint `/classify` que aceita solicitações POST. A função `classify` recebe os dados da requisição em formato JSON, verifica se o algoritmo foi especificado e executa a lógica de classificação com base no algoritmo selecionado.

4. **Endpoint para Servir Imagem**:
   ```python
   @app.route('/imagens/<path:filename>')
   def serve_image(filename):
       return send_from_directory(IMG_FOLDER, filename)
   ```

   - Este trecho define um endpoint `/imagens/<nome_do_arquivo>` para servir imagens armazenadas no diretório `imagens`.

5. **Execução da Aplicação**:
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', debug=True)
   ```

   - Por fim, este trecho inicia a aplicação Flask quando o arquivo `app.py` é executado diretamente. O servidor é iniciado na máquina local (`host='0.0.0.0'`) e com o modo de depuração ativado (`debug=True`).

Essa é uma visão geral do código-fonte da API Flask, mostrando como ele configura a aplicação, define endpoints para as operações de classificação e servir imagens, e inicia o servidor Flask para lidar com as solicitações HTTP.

## Contato

Para qualquer dúvida ou sugestão, entre em contato conosco na nossa comunidade do Discord ou abra uma issue em nosso repositório no GitHub.


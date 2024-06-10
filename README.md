# Documentação da API

Para executar o projeto a partir do GitHub, você pode seguir estes passos:

1. **Clonar o repositório:** Primeiro, você precisa clonar o repositório do GitHub para o seu ambiente local. Você pode fazer isso executando o seguinte comando no terminal:

    ```
    git clone https://github.com/mayarakaren/API-Flask.git
    ```

2. **Instalar as dependências:** Depois de clonar o repositório, navegue até o diretório do projeto e instale as dependências necessárias. Normalmente, as dependências Python são listadas em um arquivo `requirements.txt`. Você pode instalá-las usando o `pip`. No terminal, execute:

    ```
    cd API-Flask
    pip install -r requirements.txt
    ```

3. **Executar o servidor:** Agora que as dependências estão instaladas, você pode executar o servidor Flask. No terminal, execute:

    ```
    python app.py
    ```

Isso iniciará o servidor Flask e a sua API estará disponível localmente. Por padrão, o servidor será iniciado em `http://localhost:5000/`.

Depois de seguir esses passos, você poderá enviar solicitações para a sua API localmente para testar suas funcionalidades. Certifique-se de ter os dados necessários e os parâmetros corretos ao enviar solicitações para os endpoints.

## Introdução

Esta API oferece funcionalidades para classificação de dados usando diferentes algoritmos de aprendizado de máquina. Atualmente, suporta os seguintes algoritmos:

- **KNN (K-Nearest Neighbors)**
- **Algoritmo Genético**
- **Árvore de Decisão**

## Base URL

```
http://localhost:5000/
```

## Métodos

### 1. Classificação

- **Descrição:** Classifica os dados fornecidos usando o algoritmo especificado.
- **Endpoint:** `/classify`
- **Método:** POST
- **Parâmetros de Requisição:**

    | Parâmetro   | Tipo   | Descrição                                             |
    |-------------|--------|-------------------------------------------------------|
    | algorithm   | string | O algoritmo a ser utilizado (knn, algGenetico, arvore) |
    | filePath    | string | (Somente para algoritmo 'arvore') Caminho do arquivo contendo os dados (opcional) |

- **Corpo da Requisição:**

    ```json
    {
        "algorithm": "knn"
    }
    ```

- **Resposta de Sucesso:**

    ```json
    {
        "output": "Resultado da classificação",
        "acurácia": "Valor da acurácia (N/A se não aplicável)",
        "imagem": "URL para a imagem de saída (se aplicável)"
    }
    ```

- **Resposta de Erro:**

    ```json
    {
        "erro": "Descrição do erro"
    }
    ```

### 2. Servir Imagem

- **Descrição:** Retorna uma imagem armazenada no servidor.
- **Endpoint:** `/imagens/<path:filename>`
- **Método:** GET
- **Parâmetros de Requisição:**

    | Parâmetro | Tipo   | Descrição              |
    |-----------|--------|------------------------|
    | filename  | string | Nome do arquivo de imagem |

---

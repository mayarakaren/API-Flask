# models/knn.py
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

def knn():
    try:
        # Carrega a base de dados iris diretamente do caminho especificado
        file_path = "bases/iris.data"
        col_names = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
        dados = pd.read_csv(file_path, header=None, names=col_names, skiprows=1)  # Ignora a primeira linha

        # Define os atributos (X) e o rótulo (Y)
        X = np.array(dados.iloc[:, 0:4])  # Colunas de 0 a 3 são as features
        Y = np.array(dados['class'])  # Coluna 4 é a classe

        # Divide os dados em treino e teste
        X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, Y, test_size=.3, train_size=.7, random_state=42)

        # Define os valores de k a serem testados
        neighboors = [3, 5, 7]
        acuracias = []
        output = ""

        # Testa cada valor de k
        for n in neighboors:
            knn = KNeighborsClassifier(n_neighbors=n)
            knn.fit(X_TRAIN, Y_TRAIN)
            previsoes = knn.predict(X_TEST)
            acuracia = accuracy_score(Y_TEST, previsoes) * 100
            result = f"Vizinho {n}, teve a taxa de acerto de {acuracia:.2f}%"
            print(result)
            output += result + "\n"
            acuracias.append(acuracia)

        # Determina o melhor valor de k
        melhor_vizinho = neighboors[np.argmax(acuracias)]
        acuracia_melhor_vizinho = max(acuracias)
        result = f"\nMelhor vizinho foi o: {melhor_vizinho}, com a taxa de acerto de {acuracia_melhor_vizinho:.2f}%"
        print(result)
        output += result + "\n"

        # Retornar as informações adicionais
        return {
            "quantidade_exemplos": len(dados),
            "quantidade_classes": len(dados['class'].unique()),
            "quantidade_atributos": len(col_names) - 1,
            "taxa_acerto": acuracia_melhor_vizinho,
            "output": output
        }
    except Exception as e:
        return {"erro": str(e)}

# Executa a função knn e armazena o resultado
resultado_knn = knn()
print(resultado_knn)

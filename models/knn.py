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
            result = "Vizinho {}, teve a taxa de acerto de {:.2f}%".format(n, acuracia)
            print(result)
            output += result + "\n"
            acuracias.append(acuracia)

        # Determina o melhor valor de k
        melhor_vizinho = neighboors[np.argmax(acuracias)]
        acuracia_melhor_vizinho = max(acuracias)
        result = "\nMelhor vizinho foi o: {}, com a taxa de acerto de {:.2f}%".format(melhor_vizinho, acuracia_melhor_vizinho)
        print(result)
        output += result + "\n"
        
        return output
    except Exception as e:
        return f"Erro: {str(e)}"

# Executa a função knn
resultado_knn = knn()
print(resultado_knn)

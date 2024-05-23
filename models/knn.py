from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

def knn():
    dados = pd.read_csv('bases/iris.data')
    dados.dropna(inplace=True)
    X = np.array(dados.iloc[:, 0:3]) 
    Y = np.array(dados['class']) 
    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, Y, test_size=.3, train_size=.7)
    neighboors = [3, 5, 7]
    acuracias = []
    for n in neighboors:
        knn = KNeighborsClassifier(n_neighbors=n)
        knn.fit(X_TRAIN, Y_TRAIN)
        previsoes = knn.predict(X_TEST)
        acuracia = accuracy_score(Y_TEST, previsoes) * 100
        print("Vizinho {}, teve a taxa de acerto de {:.2f}%".format(n, acuracia))
        acuracias.append(acuracia)
    melhor_vizinho = neighboors[np.argmax(acuracias)]
    acuracia_melhor_vizinho = max(acuracias)
    print("\nMelhor vizinho foi o: {}, com a taxa de acerto de {:.2f}%".format(melhor_vizinho, acuracia_melhor_vizinho))

knn()
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import os

def arvore(img_folder):
    # Carregar os dados do arquivo previsao.data
    df = pd.read_csv('bases/previsao.data')

    # Dividir dados em features e target
    X = df.drop("Previsao", axis=1)
    y = df["Previsao"]

    # Dividir dados em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de Árvore de Decisão
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = clf.predict(X_test)

    # Calcular a acurácia do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Taxa de acurácia: {accuracy * 100:.2f}%')

    # Visualizar a árvore
    plt.figure(figsize=(10,6))  # Ajuste o tamanho da figura conforme necessário
    plot_tree(clf, feature_names=X.columns, class_names=clf.classes_, filled=True, rounded=True, proportion=True, fontsize=10)
    plt.title("Árvore de Decisão para Previsão de Chuva")
    img_path = os.path.join(img_folder, 'decision_tree.png')
    plt.savefig(img_path)
    plt.close()
    
    return accuracy, img_path

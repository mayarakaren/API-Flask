import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import os

def arvore(save_path="img/decision_tree_plot.png"):
    df = pd.read_csv('bases/previsao.data')

    X = df.drop("Previsao", axis=1)
    y = df["Previsao"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Taxa de acurácia: {accuracy * 100:.2f}%')

    plt.figure(figsize=(10, 6))
    plot_tree(clf, feature_names=X.columns, class_names=clf.classes_, filled=True, rounded=True, proportion=True, fontsize=10)
    plt.title("Árvore de Decisão para Previsão de Chuva")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    return accuracy, save_path

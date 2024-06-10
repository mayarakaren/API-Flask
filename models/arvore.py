import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import os

def arvore(file_path, img_folder):
    try:
        if not os.path.exists(file_path):
            return None, None

        df = pd.read_csv(file_path)
        column_names = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
        df.columns = column_names

        if df.empty:
            return None, None

        X = df.drop("class", axis=1)
        y = df["class"]
        X = X.apply(pd.to_numeric)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = DecisionTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        plt.figure(figsize=(20, 18))  # Ajusta o tamanho da figura para fornecer mais espaço
        plot_tree(clf, feature_names=X_train.columns, class_names=clf.classes_, filled=True, rounded=True, proportion=True, fontsize=16)
        plt.title("Árvore de Decisão para Classificação das Espécies de Íris", fontsize=16, pad=80)

        plt.tight_layout() 

        if not os.path.exists(img_folder):
            os.makedirs(img_folder)

        img_path = os.path.join(img_folder, 'decision_tree.png')
        plt.savefig(img_path)
        plt.close()

        return accuracy, img_path
    except Exception as e:
        return None, None

# Exemplo de chamada da função
accuracy, img_path = arvore('bases/iris.data', 'imagens')
print(f"Acurácia: {accuracy}, Caminho da imagem: {img_path}")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import os

def arvore(file_path, img_folder):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return "O DataFrame está vazio."

        X = df.drop("Previsao", axis=1)
        y = df["Previsao"]

        X = X.apply(pd.to_numeric)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = DecisionTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        plt.figure(figsize=(10, 6))
        plot_tree(clf, feature_names=X.columns, class_names=clf.classes_, filled=True, rounded=True, proportion=True, fontsize=10)
        plt.title("Árvore de Decisão")

        if not os.path.exists(img_folder):
            os.makedirs(img_folder)

        img_path = os.path.join(img_folder, 'decision_tree.png')
        plt.savefig(img_path)
        plt.close()

        return accuracy, img_path
    except Exception as e:
        return f"Erro: {str(e)}", ""

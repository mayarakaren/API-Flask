import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

class GeneticAlgorithm:
    def __init__(self):
        self.tamanho_populacao = 60
        self.populacao = []
        self.num_geracoes = 10
        self.num_filhos = 30
        self.filhos = []
        self.mutacao = 0.1
        self.all_populations = []

    def avaliar_individuo(self, x1, x2):
        return 837.9658 - (self.avaliar_ponto(x1) + self.avaliar_ponto(x2))

    def avaliar_ponto(self, x):
        return x**2 * np.sin(np.sqrt(abs(x)))

    def create_population(self):
        self.populacao = []
        for i in range(self.tamanho_populacao):
            x1 = random.uniform(-500, 500)
            x2 = random.uniform(-500, 500)
            fitness = self.avaliar_individuo(x1, x2)
            individual = [x1, x2, fitness]
            self.populacao.append(individual)

    def selecionar_pais(self):
        fitness_total = sum(individuo[2] for individuo in self.populacao)
        pesos = [individuo[2] / fitness_total for individuo in self.populacao]
        pai1 = random.choices(self.populacao, weights=pesos, k=1)[0]
        pai2 = random.choices(self.populacao, weights=pesos, k=1)[0]
        return pai1, pai2

    def realizar_mutacao(self, filho):
        for i in range(2):
            if random.random() < self.mutacao:
                filho[i] = random.uniform(-500, 500)
        filho[2] = self.avaliar_individuo(filho[0], filho[1])
        return filho

    def realizar_descarte(self):
        self.populacao.sort(key=lambda x: x[2])
        self.populacao = self.populacao[:self.num_filhos]

    def verificar_melhor_individuo(self, geracao):
        melhor_individuo = min(self.populacao, key=lambda x: x[2])
        output = (
            "======================================\n"
            f"Geração: {geracao}\n"
            f"Tamanho da População: {self.num_filhos}\n"
            "O melhor indivíduo:\n"
            f"X = {melhor_individuo[0]}\n"
            f"Y = {melhor_individuo[1]}\n"
            f"Fitness = {melhor_individuo[2]}\n\n"
        )
        print(output)
        return melhor_individuo

    def reproduzir(self):
        self.filhos = []
        for _ in range(self.num_filhos // 2):
            pai1, pai2 = self.selecionar_pais()
            xf1, yf1 = pai1[:2]
            xf2, yf2 = pai2[:2]

            filho1 = [xf1, yf1, 0]
            filho2 = [xf2, yf2, 0]

            filho1 = self.realizar_mutacao(filho1)
            filho2 = self.realizar_mutacao(filho2)

            self.filhos.append(filho1)
            self.filhos.append(filho2)

    def init_execution(self):
        self.create_population()
        for contador_geracoes in range(1, self.num_geracoes + 1):
            self.reproduzir()
            self.populacao.extend(self.filhos)
            self.realizar_descarte()
            self.all_populations.append(self.populacao.copy())
            melhor_individuo = self.verificar_melhor_individuo(contador_geracoes)
        return melhor_individuo

    def plot_fitness(self, img_folder):
        x = np.linspace(-500, 500, 100)
        y = np.linspace(-500, 500, 100)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)

        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                z[i, j] = 837.9658 - (self.avaliar_ponto(x[i, j]) + self.avaliar_ponto(y[i, j]))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

        x_coordinate = [individual[0] for individual in self.populacao]
        y_coordinate = [individual[1] for individual in self.populacao]
        costs = [individual[2] for individual in self.populacao]
        ax.scatter(x_coordinate, y_coordinate, costs, color='red', label='Ótimos pontos')

        best = min(self.populacao, key=lambda x: x[2])
        ax.scatter(best[0], best[1], best[2], color='blue', s=100, label='O melhor indíviduo')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Custo')
        ax.set_title('Superfície da função custo')

        plt.legend()

        # Verificar se o diretório de imagens existe, caso contrário, criar
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)

        img_path = os.path.join(img_folder, 'genetic_algorithm.png')
        plt.savefig(img_path)
        plt.close()
        return img_path

def run_genetic_algorithm(img_folder):
    algorithm_instance = GeneticAlgorithm()
    best_individual = algorithm_instance.init_execution()
    image_path = algorithm_instance.plot_fitness(img_folder)
    return best_individual, image_path

# Exemplo de chamada da função
best_individual, image_path = run_genetic_algorithm('imagens')
print(f"Melhor indivíduo: {best_individual}, Caminho da imagem: {image_path}")

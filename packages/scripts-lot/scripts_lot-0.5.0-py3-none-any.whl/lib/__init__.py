from lib import Script

class Script:
    @staticmethod
    def get_ga_text():
        return "GA"

    @staticmethod
    def get_kmeans_text():
        return "KMEANS"





lib
import random

# Initial weights and values
items = [(3, 266), (13, 442), (10, 671), (9, 526), (7, 388), (1, 245), (8, 210), (8, 145), (2, 126), (9, 322)]

knapsack_weight = 35

population = [
    [0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
]
     

def fitness(chromosome):
    weight = 0
    value = 0
    for i, gene in enumerate(chromosome):
        if gene == 1:
            weight += items[i][0]
            value += items[i][1]
    if weight > knapsack_weight:
        return 0
    else:
        return value

def crossover(parent1, parent2):
    point1 = random.randint(0, len(parent1) - 1)
    point2 = random.randint(0, len(parent1) - 1)
    if point1 > point2:
        point1, point2 = point2, point1
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return offspring1, offspring2


def mutation(chromosome):
    point1 = random.randint(0, len(chromosome) - 1)
    point2 = random.randint(0, len(chromosome) - 1)
    if point1 == point2:
        point2 = (point2 + 1) % len(chromosome)
    chromosome[point1] = 1 - chromosome[point1]
    chromosome[point2] = 1 - chromosome[point2]
    return chromosome


def genetic_algorithm():
    best_chromosomes = sorted(population, key=fitness, reverse=True)[:4]
    # Generate new offspring
    offspring = []
    for i in range(4):
        parent1 = random.choice(best_chromosomes)
        parent2 = random.choice(best_chromosomes)
        offspring1, offspring2 = crossover(parent1, parent2)
        offspring.append(mutation(offspring1))
        offspring.append(mutation(offspring2))
    best_offspring = sorted(offspring, key=fitness, reverse=True)[:4]
    new_population = best_chromosomes + best_offspring
    for i in range(15):
        best_chromosomes = sorted(new_population, key=fitness, reverse=True)[:4]
        offspring = []
        for i in range(4):
            parent1 = random.choice(best_chromosomes)
            parent2 = random.choice(best_chromosomes)
            offspring1, offspring2 = crossover(parent1, parent2)
            offspring.append(mutation(offspring1))
            offspring.append(mutation(offspring2))
        best_offspring = sorted(offspring, key=fitness, reverse=True)[:4]
        new_population = best_chromosomes + best_offspring
    best_chromosome = sorted(new_population, key=fitness, reverse=True)[0]
    print("Best chromosome:", best_chromosome)
    print("Total value:", fitness(best_chromosome))
     

genetic_algorithm()


# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================



class KMeans:
    def __init__(self, n_clusters=5, max_iter=300, random_state=0):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None

    def fit(self, X):
        # Set random seed
        np.random.seed(self.random_state)

        # Initialize centroids randomly
        n_samples, n_features = X.shape
        idx = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[idx]

        # Initialize variables
        prev_centroids = None
        self.labels_ = np.zeros(n_samples)

        # Main loop
        for _ in range(self.max_iter):
            # Assign points to nearest centroid
            for i in range(n_samples):
                distances = np.sqrt(np.sum((X[i] - self.centroids)**2, axis=1))
                self.labels_[i] = np.argmin(distances)

            # Store previous centroids
            prev_centroids = self.centroids.copy()

            # Update centroids
            for i in range(self.n_clusters):
                points = X[self.labels_ == i]
                if len(points) > 0:
                    self.centroids[i] = np.mean(points, axis=0)

            # Check convergence
            if np.all(prev_centroids == self.centroids):
                break

        return self

    def predict(self, X):
        # Predict cluster labels for new data
        n_samples = X.shape[0]
        labels = np.zeros(n_samples)

        for i in range(n_samples):
            distances = np.sqrt(np.sum((X[i] - self.centroids)**2, axis=1))
            labels[i] = np.argmin(distances)

        return labels


# Create feature matrix
X = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].values

# Initialize and fit KMeans
kmeans = KMeans(n_clusters=5, max_iter=300, random_state=0)
kmeans.fit(X)

# Add cluster labels to dataframe
df['Cluster'] = kmeans.labels_



# Visualize the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster', data=df, palette='Set1', s=100)

plt.title('Clusters of customers')
plt.grid(True)
plt.show()


# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================


import math

def minimax(depth, is_maximizing, board, evaluate, possible_moves):
    """
    Minimax algorithm to choose the best move.

    Parameters:
        depth (int): Current depth in the game tree.
        is_maximizing (bool): True if maximizing player's turn, False otherwise.
        board (list): Current state of the game board.
        evaluate (function): Function to evaluate the board.
        possible_moves (function): Function to generate all possible moves.

    Returns:
        best_score (int): The score of the best move.
    """
    # Base case: return the evaluation of the board
    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if is_maximizing:
        best_score = -math.inf
        for move in possible_moves(board):
            make_move(board, move, maximizing_player=True)
            score = minimax(depth - 1, False, board, evaluate, possible_moves)
            undo_move(board, move)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in possible_moves(board):
            make_move(board, move, maximizing_player=False)
            score = minimax(depth - 1, True, board, evaluate, possible_moves)
            undo_move(board, move)
            best_score = min(best_score, score)
        return best_score

# Example Game Functions
def is_terminal(board):
    # Check if the game is over (win/loss/draw)
    return len(possible_moves(board)) == 0

def evaluate(board):
    # Dummy evaluation function for demonstration (to be replaced by actual logic)
    # Positive score for the maximizing player, negative for minimizing.
    return sum(board)

def possible_moves(board):
    # Returns a list of possible moves for the current board
    return [i for i, spot in enumerate(board) if spot == 0]

def make_move(board, move, maximizing_player):
    # Make a move on the board
    board[move] = 1 if maximizing_player else -1

def undo_move(board, move):
    # Undo a move on the board
    board[move] = 0

# Example Usage
if __name__ == "__main__":
    # A sample game board (1 = Maximizing player, -1 = Minimizing player, 0 = Empty)
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 3x3 Tic-Tac-Toe board

    # Depth of search
    depth = 4

    # Find the best move
    best_score = -math.inf
    best_move = None
    for move in possible_moves(board):
        make_move(board, move, maximizing_player=True)
        move_score = minimax(depth - 1, False, board, evaluate, possible_moves)
        undo_move(board, move)
        if move_score > best_score:
            best_score = move_score
            best_move = move

    print("Best Move:", best_move)
    print("Best Score:", best_score)



# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================



import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min

def k_medoids(X, k, max_iter=100, random_state=None):
    # Set the random seed for reproducibility
    np.random.seed(random_state)
    
    # Step 1: Randomly initialize the medoids by selecting k data points
    n_samples = X.shape[0]
    medoids = X[np.random.choice(n_samples, k, replace=False)]
    
    for iteration in range(max_iter):
        # Step 2: Assign each point to the nearest medoid
        dist_matrix = np.linalg.norm(X[:, np.newaxis] - medoids, axis=2)
        labels = np.argmin(dist_matrix, axis=1)
        
        # Step 3: Update medoids
        new_medoids = np.copy(medoids)
        for i in range(k):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                # Calculate the cost of choosing each point in the cluster as the new medoid
                costs = np.sum(np.linalg.norm(cluster_points[:, np.newaxis] - cluster_points, axis=2), axis=1)
                new_medoids[i] = cluster_points[np.argmin(costs)]
        
        # Check for convergence (if medoids do not change)
        if np.all(medoids == new_medoids):
            break
        
        medoids = new_medoids
        
    return labels, medoids

# Example usage:
# X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])  # Sample data
# k = 2  # Number of clusters
# labels, medoids = k_medoids(X, k)

# print("Labels:", labels)
# print("Medoids:", medoids)




# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================



Plottings

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Generate sample data
np.random.seed(0)
x = np.linspace(0, 10, 100)
y = np.sin(x) + 0.2 * np.random.randn(100)
data = np.random.normal(loc=0, scale=1, size=1000)

# Create a dataframe for seaborn
df = pd.DataFrame({
    'Category': np.random.choice(['A', 'B', 'C'], size=100),
    'Value': np.random.rand(100)
})

# Create the figure and subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Scatter plot
axes[0, 0].scatter(x, y, color='blue', alpha=0.5)
axes[0, 0].set_title('Scatter Plot')

# Line plot
axes[0, 1].plot(x, y, color='green', linewidth=2)
axes[0, 1].set_title('Line Plot')

# Bar plot
sns.barplot(x='Category', y='Value', data=df, ax=axes[0, 2], palette='Set1')
axes[0, 2].set_title('Bar Plot')

# Histogram
axes[1, 0].hist(data, bins=30, color='purple', alpha=0.7)
axes[1, 0].set_title('Histogram')

# Box plot
sns.boxplot(data=data, ax=axes[1, 1], color='orange')
axes[1, 1].set_title('Box Plot')

# Violin plot
sns.violinplot(data=data, ax=axes[1, 2], color='pink')
axes[1, 2].set_title('Violin Plot')

# Adjust layout
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd





# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================





# Create a more complex dataset
np.random.seed(0)
categories = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(10, 100, size=5)
x = np.random.rand(100) * 10  # Random x values for scatter plot
y = 2 * x + np.random.randn(100) * 2  # Correlated y values with some noise

# Create a dataframe for better structure (for the bar plot)
df = pd.DataFrame({
    'Category': categories,
    'Value': values
})

# Create the figure and axis
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Bar Plot
axes[0].bar(df['Category'], df['Value'], color='teal')
axes[0].set_title('Bar Plot')
axes[0].set_xlabel('Category')
axes[0].set_ylabel('Value')

# Scatter Plot
axes[1].scatter(x, y, color='red', alpha=0.6)
axes[1].set_title('Scatter Plot')
axes[1].set_xlabel('X Value')
axes[1].set_ylabel('Y Value')

# Adjust layout for better spacing
plt.tight_layout()
plt.show()

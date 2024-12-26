import matplotlib.pyplot as plt

def plot_bar(data, labels):
    """Génère un graphique en barres."""
    plt.bar(labels, data)
    plt.show()

def plot_histogram(data):
    """Génère un histogramme."""
    plt.hist(data, bins=10)
    plt.show()

def plot_scatter(x, y):
    """Génère un graphique de dispersion."""
    plt.scatter(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graphique de dispersion')
    plt.show()

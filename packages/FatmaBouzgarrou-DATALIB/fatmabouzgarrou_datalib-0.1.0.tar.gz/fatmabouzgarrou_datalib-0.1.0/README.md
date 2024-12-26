# DataLib

**DataLib** est une bibliothèque Python simple pour la manipulation, l'analyse et la visualisation des données. Elle fournit des outils pratiques pour normaliser des données, gérer les valeurs manquantes, calculer des statistiques descriptives et créer des visualisations courantes.

## Fonctionnalités

- **Chargement et traitement des données** :
  - Chargement de fichiers CSV.
  - Normalisation des colonnes numériques.
  - Gestion des valeurs manquantes (remplissage ou suppression).
  
- **Statistiques descriptives** :
  - Calcul de la moyenne, médiane et écart-type.
  - Analyse des corrélations entre colonnes.

- **Visualisation** :
  - Histogrammes.
  - Matrices de corrélation.

## Installation

Vous pouvez installer la bibliothèque directement via pip après publication sur PyPI :

```bash
pip install datalib
```


## Exemples  d'utilisation

### 1. Chargement et traitement des données

**Charger un fichier CSV :**

```python
import DataLib

data = DataLib.load_csv("path_to_file.csv")
```

**Normaliser les colonnes numériques :**

```python
normalized_data = DataLib.normalize(data)
```

**Gérer les valeurs manquantes (remplissage avec la moyenne) :**

```python
clean_data = DataLib.fill_missing_values(normalized_data, method='mean')
```

### 2. Statistiques descriptives

**Calculer la moyenne, la médiane et l'écart-type :**

```python
mean = DataLib.mean(data)
median = DataLib.median(data)
std_dev = DataLib.std(data)
```

**Analyser les corrélations entre les colonnes :**

```python
correlation_matrix = DataLib.correlation(data)
```

### 3. Visualisation des données

**Créer un histogramme pour une colonne spécifique :**

```python
DataLib.plot_histogram(data, column='age')
```

**Créer une matrice de corrélation :**

```python
DataLib.plot_correlation_matrix(data)
```
```

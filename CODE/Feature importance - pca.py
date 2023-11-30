import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load the data
file_path = '/Users/joudathashmi/Downloads/liveability.csv'
suburbs_data_pca = pd.read_csv(file_path)

# Calculate mean only for numeric columns
numeric_columns_mean = suburbs_data_pca.select_dtypes(include=[np.number]).mean()

# Fill missing values in numeric columns with their respective means
suburbs_data_pca_filled = suburbs_data_pca.fillna(numeric_columns_mean)

# Normalize the data
# Dropping the 'suburb' column for PCA
data_for_pca = suburbs_data_pca_filled.drop('suburb', axis=1)
scaler_pca = StandardScaler()
normalized_data_pca = scaler_pca.fit_transform(data_for_pca)

# Perform PCA
pca = PCA()
pca.fit(normalized_data_pca)

# Calculate the explained variance ratio of the PCA components
explained_variance = pca.explained_variance_ratio_

# Calculate the cumulative variance explained
cumulative_variance = np.cumsum(explained_variance)

# Plotting the cumulative variance
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o')
plt.title('Cumulative Variance Explained by PCA Components')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Variance Explained')
plt.grid(True)
plt.show()

# Transform the data to the first two principal components
pca_transformed = pca.transform(normalized_data_pca)

# Plotting the first two principal components
plt.figure(figsize=(10, 6))
plt.scatter(pca_transformed[:, 0], pca_transformed[:, 1])
plt.title('First Two Principal Components')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()

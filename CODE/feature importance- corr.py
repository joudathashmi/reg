import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
file_path = '/Users/joudathashmi/Downloads/liveability.csv'  # Update this with the path to your file
suburbs_data = pd.read_csv(file_path)

# Select only numeric columns for correlation calculation
numeric_suburbs_data = suburbs_data.select_dtypes(include=[np.number])

# Handle missing values by filling with the mean of numeric columns
numeric_suburbs_data_filled = numeric_suburbs_data.fillna(numeric_suburbs_data.mean())

# Calculate the correlation matrix
correlation_matrix = numeric_suburbs_data_filled.corr()

# Display the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Plotting the heatmap for the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title("Correlation Matrix Heatmap")
plt.show()

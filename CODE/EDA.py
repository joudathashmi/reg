
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
# Load the data
file_path = '/Users/joudathashmi/Downloads/liveability.csv'  # Update this with the path to your file
data = pd.read_csv(file_path)

ßßßß
# Displaying basic information about the dataset
info = data.info()
first_rows = data.head()

# Setting the aesthetics for the plots
sns.set(style="whitegrid")

# Scatter plot for Median Price vs Liveability
plt.figure(figsize=(12, 6))
sns.scatterplot(data=data, x='Median Price', y='Liveability')
plt.title('Median Price vs Liveability')
plt.xlabel('Median Price')
plt.ylabel('Liveability')
plt.show()

# Scatter plot for Traffic vs Liveability
plt.figure(figsize=(12, 6))
sns.scatterplot(data=data, x='Traffic', y='Liveability')
plt.title('Traffic vs Liveability')
plt.xlabel('Traffic')
plt.ylabel('Liveability')
plt.show()

# Bar chart for average Liveability by Public Transport rating
avg_liveability_by_public_transport = data.groupby('Public Transport')['Liveability'].mean().sort_index()
plt.figure(figsize=(12, 6))
avg_liveability_by_public_transport.plot(kind='bar')
plt.title('Average Liveability by Public Transport Rating')
plt.xlabel('Public Transport Rating')
plt.ylabel('Average Liveability')
plt.xticks(rotation=0)
plt.show()

# Bar chart for average Liveability by Safety rating
avg_liveability_by_safety = data.groupby('Safety')['Liveability'].mean().sort_index()
plt.figure(figsize=(12, 6))
avg_liveability_by_safety.plot(kind='bar')
plt.title('Average Liveability by Safety Rating')
plt.xlabel('Safety Rating')
plt.ylabel('Average Liveability')
plt.xticks(rotation=0)
plt.show()

# Print basic information and the first few rows of the dataset
print(info)
print(first_rows)

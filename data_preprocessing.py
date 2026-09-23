import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv('path_to_your_dataset.csv')

# Preprocess data
# Example: Handle missing values
df.fillna(df.mean(), inplace=True)

# Split data into features and target
X = df.drop('target_column', axis=1)
y = df['target_column']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('Data preprocessing complete.')

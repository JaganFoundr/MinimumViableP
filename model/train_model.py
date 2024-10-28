import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
data = pd.read_csv('data/investment_data.csv')

# Encode categorical variables
le_risk = LabelEncoder()
le_choice = LabelEncoder()
data['Risk_Tolerance'] = le_risk.fit_transform(data['Risk_Tolerance'])
data['Investment_Choice'] = le_choice.fit_transform(data['Investment_Choice'])

# Features and Labels
X = data[['Income', 'Savings', 'Risk_Tolerance']]
y = data['Investment_Choice']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'investment_model.pkl')

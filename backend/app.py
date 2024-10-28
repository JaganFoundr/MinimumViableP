from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
model = joblib.load('model/investment_model.pkl')

# Define a mapping from country codes to currencies (can be expanded)
currency_map = {
    'USD': 'United States Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'INR': 'Indian Rupee',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'JPY': 'Japanese Yen',
    # Add more currencies as necessary
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    income = user_data['income']
    savings = user_data['savings']
    risk_tolerance = user_data['risk_tolerance']
    country = user_data['country']  # Get country from the request

    # Prepare input for the model
    input_data = np.array([[income, savings, risk_tolerance]])
    
    # Predict the investment recommendation
    prediction = model.predict(input_data)
    
    # Map integer predictions back to investment choices
    investment_choices = ['Tech Stocks', 'Index Funds', 'Government Bonds', 'Real Estate', 'Mutual Funds']
    recommended_investment = investment_choices[prediction[0]]
    
    # Determine the currency based on the selected country
    currency = currency_map.get(country, 'Unknown Currency')
    
    return jsonify({'recommendations': [recommended_investment], 'currency': currency})

if __name__ == '__main__':
    app.run(debug=True)

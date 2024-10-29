from flask import Flask, request, render_template
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load pre-trained model and tokenizer from Hugging Face
model_name = "EleutherAI/gpt-neo-1.3B"  # Change to your preferred model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define a mapping from country codes to currencies (can be expanded)
currency_map = {
    'USD': 'United States Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'INR': 'Indian Rupee',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'JPY': 'Japanese Yen',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get data from the form
    income = request.form['income']
    savings = request.form['savings']
    risk_tolerance = request.form['risk_tolerance']
    country = request.form['country']

    # Create a prompt for the LLM
    prompt = (
        f"Based on the following financial information:\n"
        f"Annual Income: {income}\n"
        f"Savings: {savings}\n"
        f"Risk Tolerance: {risk_tolerance}\n"
        f"Country: {currency_map[country]}\n\n"
        f"Provide personalized investment recommendations."
    )

    # Tokenize input and generate output
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    try:
        # Generate recommendations
        output = model.generate(input_ids, max_length=150, num_return_sequences=1)
        recommendations = tokenizer.decode(output[0], skip_special_tokens=True).strip().split('\n')

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        recommendations = ["Unable to generate recommendations at this time."]

    # Determine the currency based on the selected country
    currency = currency_map.get(country, 'Unknown Currency')

    print(f"Recommendations: {recommendations}, Currency: {currency}")
    
    # Render the recommendation page with the results
    return render_template('recommendation.html', recommendations=recommendations, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)

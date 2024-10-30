from flask import Flask, request, render_template
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load pre-trained model and tokenizer from Hugging Face
model_name = "meta-llama/LLaMA-3.2-1B"  # Replace with your actual model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the pad token to the EOS token if no pad token is defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

# Define a mapping from country codes to currencies
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
    income = request.form.get('income', 'N/A')
    savings = request.form.get('savings', 'N/A')
    risk_tolerance = request.form.get('risk_tolerance', 'N/A')
    country = request.form.get('country', 'USD')

    # Create a prompt for the LLM
    prompt = (
        f"Based on the following financial information:\n"
        f"Annual Income: {income}\n"
        f"Savings: {savings}\n"
        f"Risk Tolerance: {risk_tolerance}\n"
        f"Country: {currency_map.get(country, 'United States Dollar')}\n\n"
        f"Provide personalized investment recommendations."
    )

    # Tokenize input with padding and truncation
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

    try:
        # Generate recommendations
        output = model.generate(
            **inputs, 
            max_length=150, 
            num_return_sequences=1, 
            do_sample=True, 
            temperature=0.7
        )
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
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, render_template
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load pre-trained model and tokenizer from Hugging Face
model_name = "meta-llama/LLaMA-3.2-1B"  # Replace with your actual model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the pad token to the EOS token if no pad token is defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

# Define a mapping from country codes to currencies
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
    income = request.form.get('income', 'N/A')
    savings = request.form.get('savings', 'N/A')
    risk_tolerance = request.form.get('risk_tolerance', 'N/A')
    country = request.form.get('country', 'USD')

    # Create a prompt for the LLM
    prompt = (
        f"Based on the following financial information:\n"
        f"Annual Income: {income}\n"
        f"Savings: {savings}\n"
        f"Risk Tolerance: {risk_tolerance}\n"
        f"Country: {currency_map.get(country, 'United States Dollar')}\n\n"
        f"Provide personalized investment recommendations."
    )

    # Tokenize input with padding and truncation
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

    try:
        # Generate recommendations
        output = model.generate(
            **inputs, 
            max_length=150, 
            num_return_sequences=1, 
            do_sample=True, 
            temperature=0.7
        )
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
    app.run(host='0.0.0.0', port=5000, debug=True)

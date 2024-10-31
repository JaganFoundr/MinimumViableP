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
    income = request.form.get('income')
    savings = request.form.get('savings')
    risk_tolerance = request.form.get('risk_tolerance')
    country = request.form.get('country', 'USD')

    # Validate input
    if not income.isdigit() or not savings.isdigit() or int(income) <= 0 or int(savings) < 0:
        return render_template('index.html', error="Invalid income or savings input.")

    # Create a structured prompt for the LLM
    prompt = (
        f"Consider the following individual's financial profile and provide tailored investment advice:\n\n"
        f"1. **Annual Income**: {income}\n"
        f"2. **Savings**: {savings}\n"
        f"3. **Risk Tolerance**: {risk_tolerance}\n"
        f"4. **Location**: {currency_map.get(country, 'United States Dollar')}\n\n"
        f"Provide a structured investment strategy:\n"
        f"- Asset Allocation\n"
        f"- Risk Management\n"
        f"- Short-Term and Long-Term Goals\n"
        f"- Any specific recommendations for {currency_map.get(country)}."
    )

    # Tokenize input and generate output
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    
    try:
        # Generate recommendations
        output = model.generate(
            **inputs,
            max_length=200,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )
        raw_recommendation = tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # Split recommendations into structured sections (example split logic)
        structured_recommendation = {
            "Asset Allocation": raw_recommendation.split("Risk Management")[0].strip(),
            "Risk Management": raw_recommendation.split("Risk Management")[1].split("Short-Term and Long-Term Goals")[0].strip(),
            "Short-Term and Long-Term Goals": raw_recommendation.split("Short-Term and Long-Term Goals")[1].strip()
        }

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        structured_recommendation = {
            "Asset Allocation": "Unable to provide asset allocation advice at this time.",
            "Risk Management": "Unable to provide risk management advice at this time.",
            "Short-Term and Long-Term Goals": "Unable to provide short- and long-term goals advice at this time."
        }

    currency = currency_map.get(country, 'Unknown Currency')

    # Render the recommendation page with the structured recommendations
    return render_template(
        'recommendation.html',
        recommendations=structured_recommendation,
        currency=currency
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

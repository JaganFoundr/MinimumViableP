from flask import Flask, request, render_template
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load pre-trained model and tokenizer
model_name = "meta-llama/LLaMA-3.2-1B"  # Replace with your actual model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Ensure correct padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user profile input from the textarea
    profile = request.form.get('profile')

    # Use the user input directly in the prompt
    prompt = profile  # Use exactly what the user typed in the textarea

    # Tokenize input and generate output
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

    try:
        # Generate recommendations
        output = model.generate(
            **inputs,
            max_length=300,  # Adjust max length for comprehensive output
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )
        raw_recommendation = tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # You may want to consider splitting or structuring the recommendation here, if necessary
        # For now, we'll keep it as a single output
        structured_recommendation = {
            "Recommendations": raw_recommendation
        }

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        structured_recommendation = {
            "Recommendations": "Unable to provide recommendations at this time."
        }

    # Render the recommendation page with the structured recommendations
    return render_template(
        'recommendation.html',
        recommendations=structured_recommendation
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

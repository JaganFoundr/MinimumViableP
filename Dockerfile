# Use an official Python image as a base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install the Hugging Face CLI for model downloads
RUN pip install huggingface-hub

# Set Hugging Face token as a build argument and log in
ARG HF_AUTH_TOKEN
RUN huggingface-cli login --token $HF_AUTH_TOKEN

# Download the model (this will happen during build, not at runtime)
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
AutoTokenizer.from_pretrained('meta-llama/LLaMA-3.2-1B', token='$HF_AUTH_TOKEN'); \
AutoModelForCausalLM.from_pretrained('meta-llama/LLaMA-3.2-1B', token='$HF_AUTH_TOKEN')"

# Clean up Hugging Face CLI authentication by logging out and unsetting the token
RUN huggingface-cli logout && unset HF_AUTH_TOKEN

# Copy the entire project directory into the container
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

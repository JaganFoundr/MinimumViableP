from transformers import Trainer, TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# Load dataset (without streaming) and split into train/test
dataset = load_dataset('json', data_files='data.json')
split_dataset = dataset['train'].train_test_split(test_size=0.2)
train_dataset = split_dataset['train']
test_dataset = split_dataset['test']

# Load model and tokenizer
model_name = "openai-community/gpt2"  # Ensure this model exists on Hugging Face Hub
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Add padding token if missing
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})
    model.resize_token_embeddings(len(tokenizer))

# Disable cache to reduce memory usage
model.config.use_cache = False

# Tokenization function with improved handling for padding and truncation
def preprocess_function(examples):
    inputs = tokenizer(examples['input'], truncation=True, padding='max_length', max_length=32)
    outputs = tokenizer(examples['output'], truncation=True, padding='max_length', max_length=32)
    inputs['labels'] = outputs['input_ids']
    return inputs

# Tokenize datasets with improved error handling
try:
    tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
    tokenized_test_dataset = test_dataset.map(preprocess_function, batched=True)
except Exception as e:
    print(f"Error during tokenization: {e}")

# Training arguments optimized for CPU and memory limitations
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',  # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=1,  # Adjust based on available memory
    gradient_accumulation_steps=2,  # Use gradient accumulation to simulate larger batch sizes
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,  # Log every 10 steps
    save_strategy='epoch',  # Save model every epoch
    load_best_model_at_end=True,  # Load the best model at the end of training
    metric_for_best_model="loss",  # Use loss to determine best model
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_test_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')

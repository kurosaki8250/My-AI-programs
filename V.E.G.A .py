from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import os
import subprocess

# Load the model and tokenizer
model_name = "cognitivecomputations/dolphin-2.9-llama3-8b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, force_download=True)

# Load the dataset
dataset = load_dataset("open-llm-leaderboard/cognitivecomputations__dolphin-2.9-llama3-8b-details",
                       "cognitivecomputations_dolphin-2.9-llama3-8b_leaderboard_arc_challenge")

# Print the available splits
print("Available splits:", dataset.keys())

# Access data from a specific split
split_name = 'latest'  # Ensure this split exists in your dataset
if split_name in dataset:
    data_split = dataset[split_name]
    print("First data sample from the dataset:")
    print(data_split[0])
else:
    print(f"Split '{split_name}' not found in the dataset.")

# Function to generate AI response
def generate_response(prompt):
    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate response
    outputs = model.generate(inputs["input_ids"], max_length=100, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the output to a string
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to execute system commands
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"

# Helper functions for system handling
def open_file(file_name):
    try:
        os.startfile(file_name)
        return f"Opening file: {file_name}"
    except Exception as e:
        return f"Error: {str(e)}"

def open_app(app_name):
    try:
        subprocess.run(app_name, shell=True)
        return f"Opening app: {app_name}"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(file_name):
    try:
        os.remove(file_name)
        return f"Deleted file: {file_name}"
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to process user input
def process_user_input(user_input):
    user_input = user_input.lower()
    
    if "open" in user_input and "file" in user_input:
        file_name = user_input.split("file")[-1].strip()
        return open_file(file_name)
    
    elif "open" in user_input and "app" in user_input:
        app_name = user_input.split("app")[-1].strip()
        return open_app(app_name)
    
    elif "delete" in user_input and "file" in user_input:
        file_name = user_input.split("file")[-1].strip()
        return delete_file(file_name)
    
    elif "shutdown" in user_input:
        return execute_command("shutdown /s /t 0")
    
    elif "restart" in user_input:
        return execute_command("shutdown /r /t 0")
    
    else:
        return generate_response(user_input)

# Main interactive loop
if _name_ == "_main_":
    print("LLaMA-powered Virtual Assistant with Dataset Integration is ready!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = process_user_input(user_input)
        print("Assistant:", response)
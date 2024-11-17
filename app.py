from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from dotenv import load_dotenv
import os
from huggingface_hub import login
#login()
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Replace with the actual LLaMA model name
model_name = "meta-llama/Llama-3.2-1B"
token = os.getenv("HUGGING_FACE_TOKEN")  # Get the token from environment variables

# Load the tokenizer and model with the authentication token
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

# Set the padding token to be the same as the eos token
tokenizer.pad_token = tokenizer.eos_token

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=1000)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

#@app.route('/')
#def index():
#    return "Welcome to the LLaMA Chatbot!"

#@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = generate_response(user_message)
    print(response)
    return jsonify({'response': response})

if __name__ == "__main__":
    print("Chat with LLaMA! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = generate_response(user_input)
        print(f"LLaMA: {response}")
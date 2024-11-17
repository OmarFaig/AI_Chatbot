import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
#from unsloth import quantize_model
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Replace with the actual LLaMA model name
model_name = "meta-llama/Llama-3.2-3B"
token = os.getenv("HUGGING_FACE_TOKEN")  # Get the token from environment variables

# Load the tokenizer and model with the authentication token
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
print("Model loaded successfully.")

# Quantize the model
print("Quantizing model...")
#model = quantize_model(model, bits=8)
print("Model quantized successfully.")

# Set the padding token to be the same as the eos token
tokenizer.pad_token = tokenizer.eos_token

# Ensure the model is on the CPU
device = torch.device("cpu")
model.to(device)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=100,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    print("Chat with LLaMA! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = generate_response(user_input)
        print(f"LLaMA: {response}")
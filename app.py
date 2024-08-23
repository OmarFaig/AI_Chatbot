from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

model_name = "microsoft/DialoGPT-medium"  # Use a conversational model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the padding token to be the same as the eos token
tokenizer.pad_token = tokenizer.eos_token

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_length=1000)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(response)
    return response

generate_response ("What is your name")
#@app.route('/')
#def index():
#    return render_template('index.html')
#
#@app.route('/chat', methods=['POST'])
#def chat():
#    user_message = request.json.get('message')
#    response = generate_response(user_message)
#    return jsonify({'response': response})

#if __name__ == '__main__':
#    app.run(debug=True)

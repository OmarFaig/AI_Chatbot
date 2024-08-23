from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the pre-trained model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Start the conversation loop
print("Hello! I am your chatbot. Type 'quit' to exit.")
chat_history_ids = None

while True:
    # Get user input
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    # Encode the new user input and concatenate it to the chat history
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    if chat_history_ids is None:
        bot_input_ids = new_user_input_ids
    else:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

    # Print debug information
    print(f"User Input IDs: {new_user_input_ids}")
    print(f"Bot Input IDs: {bot_input_ids}")

    # Generate a response from the model
    attention_mask = torch.ones(bot_input_ids.shape, device=bot_input_ids.device)
    chat_history_ids = model.generate(
        bot_input_ids,
        attention_mask=attention_mask,
        max_length=bot_input_ids.shape[-1] + 50,  # Limit the max length to avoid infinite generation
        pad_token_id=tokenizer.eos_token_id,
       # do_sample=True,  # Allow for more varied responses
        temperature=0.1  # Control the randomness of the output
    )

    # Decode and print the response
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"Bot: {bot_response}")

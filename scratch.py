from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("AdaptLLM/finance-chat")
tokenizer = AutoTokenizer.from_pretrained("AdaptLLM/finance-chat")

# Put your input here:
user_input = '''Use this fact to answer the question: Title of each class Trading Symbol(s) Name of each exchange on which registered
Common Stock, Par Value $.01 Per Share MMM New York Stock Exchange
MMM Chicago Stock Exchange, Inc.
1.500% Notes due 2026 MMM26 New York Stock Exchange
1.750% Notes due 2030 MMM30 New York Stock Exchange
1.500% Notes due 2031 MMM31 New York Stock Exchange

Which debt securities are registered to trade on a national securities exchange under 3M's name as of Q2 of 2023?'''

# Apply the prompt template and system prompt of LLaMA-2-Chat demo for chat models (NOTE: NO prompt template is required for base models!)
our_system_prompt = "\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n" # Please do NOT change this
prompt = f"<s>[INST] <<SYS>>{our_system_prompt}<</SYS>>\n\n{user_input} [/INST]"

# # NOTE:
# # If you want to apply your own system prompt, please integrate it into the instruction part following our system prompt like this:
# your_system_prompt = "Please, check if the answer can be inferred from the pieces of context provided."
# prompt = f"<s>[INST] <<SYS>>{our_system_prompt}<</SYS>>\n\n{your_system_prompt}\n{user_input} [/INST]"

inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(model.device)
outputs = model.generate(input_ids=inputs, max_length=4096)[0]

answer_start = int(inputs.shape[-1])
pred = tokenizer.decode(outputs[answer_start:], skip_special_tokens=True)

print(pred)

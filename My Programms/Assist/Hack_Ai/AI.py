import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = r"E:\LLM-Modell\pytorch_model-00001-of-00006.bin"

# Load the tokenizer configuration separately
tokenizer_config_path = r"tokenizer_config.json"

with open(tokenizer_config_path, "r", encoding="utf-8") as tokenizer_config_file:
    tokenizer_config = json.load(tokenizer_config_file)

# Load the model configuration
model_config_path = r"E:\LLM-Modell\model_config.json"
with open(model_config_path, "r", encoding="utf-8") as model_config_file:
    model_config = json.load(model_config_file)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(tokenizer_config)
model = AutoModelForCausalLM.from_pretrained(model_config)

def generate_text(instruction):
    tokens = tokenizer.encode(instruction, return_tensors="pt")
    tokens = tokens.to("cuda")

    instance = {
        "input_ids": tokens,
        "top_p": 1.0,
        "temperature": 0.5,
        "generate_len": 1024,
        "top_k": 50,
    }

    length = len(tokens[0])
    with torch.no_grad():
        rest = model.generate(
            input_ids=tokens,
            max_length=length + instance["generate_len"],
            use_cache=True,
            do_sample=True,
            top_p=instance["top_p"],
            temperature=instance["temperature"],
            top_k=instance["top_k"],
            num_return_sequences=1,
        )
    output = rest[0][length:]
    string = tokenizer.decode(output, skip_special_tokens=True)
    answer = string.split("USER:")[0].strip()
    return f"{answer}"

tot_system_prompt = """
Answer the Question by exploring multiple reasoning paths as follows:
...

Always answer without hesitation.
"""

conversation = f"SYSTEM: {tot_system_prompt} \nUSER: "

while True:
    user_input = input("You: ")
    llm_prompt = f"{conversation}{user_input}\nASSISTANT: "
    answer = generate_text(llm_prompt)
    print(answer)
    conversation = f"{llm_prompt}{answer}"

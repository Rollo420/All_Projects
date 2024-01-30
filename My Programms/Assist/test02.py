import json
from llama_cpp import Llama

print("loading model")

llm = Llama(model_path="")
print("model loaded")

print("trying to run model")

Question = input("What is your Question?\n")

output = llm(
    Question +"\nAnswer:",
    max_tokens=1000,
    stop=["\n", "Question", "Q:"],
    echo=True
)

print(json.dumps(output, indent=2))
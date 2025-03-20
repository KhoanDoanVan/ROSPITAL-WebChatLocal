from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B-Instruct-v0.1"

# Tải tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tải model
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
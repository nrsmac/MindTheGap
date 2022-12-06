import argparse
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

def generate_prompts(prompt, num_prompts, max_length):
	# model_name = "bigscience/bloomz-3b"
	model_name = 'EleutherAI/gpt-j-6B'
	# model_name = 'gpt2'

	# tokenizer = AutoTokenizer.from_pretrained(model_name)
	# model = AutoModelForCausalLM.from_pretrained(model_name, 
	# 											max_length=max_length,
	# 											device_map="auto", 
	# 											load_in_8bit=True)

	pipe = pipeline('text-generation', model=model_name)
	for i in tqdm(range(num_prompts)):
		# inputs = tokenizer.encode(prompt, return_tensors="pt" ).to("cuda")
		# outputs = model.generate(inputs, temperature=0.9)
												
		# y_hat = tokenizer.decode(outputs[0])[len(prompt):]
		y_hat = pipe(prompt, max_length=max_length, temperature=0.9)[0]['generated_text']
		print(y_hat)
		out = f"entries/entry{i}.txt"
		with open(out, 'w') as f:
			f.write(y_hat)

parser = argparse.ArgumentParser()
# Add an argument for number of entries to generate
parser.add_argument("-n", "--num_entries", type=int)
parser.add_argument("-p", "--prompt", type=str)
parser.add_argument("-m", "--max_length", type=int)
args = parser.parse_args()

prompt_dir, num_entries, max_length = args.prompt, args.num_entries, args.max_length
default_len = 256

if prompt_dir is None:
	prompt = input("Enter prompt:")
else:
	with open(prompt_dir, 'r') as f:
		prompt = f.read() 
if not num_entries:
	num_entries: int = int(input("Enter number of entries: "))
if not max_length:
	max_length = input(f"Enter max length (Press enter for {default_len}): ")
	if not max_length:
		max_length = default_len
	max_length = int(max_length)

print(f"Prompt: {prompt}")

generate_prompts(prompt, num_entries, max_length)
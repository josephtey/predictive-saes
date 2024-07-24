import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
import csv
from datasets import load_dataset

ds = load_dataset("JeanKaddour/minipile")
num_written = 0

with open("all_sentences.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["sentence"])  # Write header
	
    for text in ds["train"]["text"]:
        sentences = sent_tokenize(text)
        for sentence in sentences:
            num_written += 1
            writer.writerow([sentence])
            
            if num_written % 1000 == 0:
                print(num_written)
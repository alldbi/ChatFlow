import pandas as pd

df = pd.read_csv("dataset/full_dataset.csv", nrows=100)

num_row = 10

print("[TITLE]: ", df["title"][num_row], '\n')
print("[INGREDIENTS]: ", df["ingredients"][num_row], '\n')
print("[DIRECTIONS]: ", df["directions"][num_row], '\n')
print("[LINK]: ", df["link"][num_row], '\n')
print("[SOURCE]: ", df["source"][num_row], '\n')
print("[NER]: ", df["NER"][num_row])

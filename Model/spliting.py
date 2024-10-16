import pickle

# Load the original PKL file
with open(r'Model\similarty.pkl', 'rb') as file:
    data = pickle.load(file)

# Define the number of parts to split into
num_parts = 2  # Change this number based on how many parts you need

# Split the data into smaller chunks
split_data = [data[i::num_parts] for i in range(num_parts)]

# Save each chunk separately as new PKL files
for idx, part in enumerate(split_data):
    with open(f'Model\similarty{idx+1}.pkl', 'wb') as part_file:
        pickle.dump(part, part_file)

print(f"File has been split into {num_parts} parts.")

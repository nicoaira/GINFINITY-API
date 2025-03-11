import requests

# Define the reference RNA structure (structure1)
ref_structure = "(((((((..(((............)))..((((.......))))..((((...))))..(((((.......))))))))))))."

# Path to your file (adjust the path as needed)
file_path = "/home/nicolas/Desktop/random_structures.txt"

# Read the file and construct a list of dot-bracket structures
with open(file_path, "r") as f:
    # Each non-empty line is assumed to be a valid dot-bracket structure
    batch_structures = [line.strip() for line in f if line.strip()]

# Create the JSON payload for batch comparison
payload = {
    "structure1": ref_structure,
    "structure2": batch_structures,
    "subgraphs": False,
    "L": None,
    "keep_paired_neighbors": False
}

# URL for the compare endpoint (adjust if necessary)
url = "http://localhost:8000/compare"

# Send the POST request
response = requests.post(url, json=payload)

# Print the results
print(response.json())

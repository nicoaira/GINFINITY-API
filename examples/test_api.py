import pandas as pd
import requests

# Load the sample data from the TSV file
samples_df = pd.read_csv("sample_structures.tsv", sep="\t")

# Assuming your TSV has columns: description, accession, structure
# Print a few rows to verify the format
print(samples_df.head())

# Define the accessions for the comparisons you want
accession1 = "URS00006DCB39_9606"
accession2 = "URS0000733374_9606"
accession3 = "URS00000478B7_9606"

# Filter the DataFrame to get the rows corresponding to the given accessions
row1 = samples_df[samples_df["accession"] == accession1].iloc[0]
row2 = samples_df[samples_df["accession"] == accession2].iloc[0]
row3 = samples_df[samples_df["accession"] == accession3].iloc[0]

# Get the dot-bracket structures from these rows
structure1 = row1["structure"]
structure2 = row2["structure"]
structure3 = row3["structure"]

# Define the API endpoint URL (adjust the port if necessary)
url = "http://localhost:8000/compare"

# Prepare payloads for the two comparisons:
# 1. Compare accession1 vs accession2
payload1 = {
    "structure1": structure1,
    "structure2": structure2,
    "subgraphs": False  # adjust options as needed
}

# 2. Compare accession1 vs accession3
payload2 = {
    "structure1": structure1,
    "structure2": structure3,
    "subgraphs": False  # adjust options as needed
}

# Send the POST requests to the API's /compare endpoint
response1 = requests.post(url, json=payload1)
response2 = requests.post(url, json=payload2)

# Print the results
print("Comparison of accession1 vs accession2:")
print(response1.json())

print("Comparison of accession1 vs accession3:")
print(response2.json())

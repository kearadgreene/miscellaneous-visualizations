## Pairwise Comparison of Authors (shared publications from PubMed)
# This code takes in a list of authors, and outputs the amount of shared publications
# (in PubMed)each author has with all the other authors.
# replace the api_key in the url = line with your NCBI API key. 
# This can be found under your account setting of your NCBI account (free to make)
# Update the authors list with the authors you want
# The directory should also be updated to your own directory (df.to_excel line)
# requires requests and pandas packages
# 
# Adapted from ChatGPT
# Keara D. Greene 11.18.24



import requests

def get_pmids(author):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='{author}'[Author]&retmax=1000&api_key=f71e710fa3dcced4882e11c99de43928a608&retmode=json" #update with your API key
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching data for {author}: {response.status_code}")
        print(f"Response content: {response.text}")
        return set()  # Return an empty set on error

    try:
        pmids = response.json().get('esearchresult', {}).get('idlist', [])
        return set(pmids)
    except ValueError:
        print(f"Error decoding JSON for {author}: {response.text}")
        return set()  # Return an empty set on JSON decode error
    
#update author list below
authors = ["Susan Whitfield-Gabrieli", "Jordan Smoller", "A Eden Evins", "Randi Schuster", "Tian Ge", "Jiahe Zhang", "Dost Öngür", "Christian Webb", "Karl Friston", "Peter Zeidman", "John Gabrieli", "Dina Katabi", "Alfonso Nieto-Castanon", "Thomas Nichols"]  # List of authors
pmid_dict = {author: get_pmids(author) for author in authors}

shared_publications = {}
for i in range(len(authors)):
    for j in range(i + 1, len(authors)):
        author1 = authors[i]
        author2 = authors[j]
        shared_count = len(pmid_dict[author1].intersection(pmid_dict[author2]))
        shared_publications[(author1, author2)] = shared_count

print(shared_publications)



import pandas as pd

# Assuming shared_publications is your dictionary with counts
# Example: shared_publications = {('Author1', 'Author2'): 5, ('Author1', 'Author3'): 2, ...}

# Convert the dictionary to a list of tuples for DataFrame creation
data = [(author1, author2, count) for (author1, author2), count in shared_publications.items()]

# Create a DataFrame
df = pd.DataFrame(data, columns=['Author 1', 'Author 2', 'Shared Publications'])

# Export the DataFrame to an Excel file
df.to_excel('/Users/kdg32/Downloads/shared_publications.xlsx', index=False) # update with your own path

print("Data has been exported.")

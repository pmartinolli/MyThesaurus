# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:00:05 2024

@author: pascaliensis, with ChatGPT 3.5

### Script Overview

TL;DR: Automatically index tags in Obsidian Markdown notes with YAML header 

**Phase 1: Preparing Tags**  
- The script reads a CSV file named `tags.csv` with two columns: `tag` and `alias`.  
- It normalizes the `tag` column to meet Obsidian.md's tag requirements (removing accents, special characters like parentheses, etc.).  
- Each row pairs a `tag` with its corresponding `alias`.  
- The CSV data is loaded into a dataframe for processing.  

Bonus : there is a script MarkdownTagHarvester.py that build a tags_a_trier.csv based on the note names (->tag) and theirs aliases (->alias)
Important: The `tags.csv` requires thorough inspection, cleaning, and validation to ensure relevance. Consult your librarian for guidance on selecting appropriate tags.

**Phase 2: Updating Notes**  
- The script scans the specified `folder_path` (and its subfolders) containing the Obsidian.md vault.  
- It opens each `.md` file, reads its content, and checks for any occurrence of the listed aliases.  
- If an alias is found, it updates the `tags` key in the YAML front matter of the note.  

Note: The script works with UTF-8 encoding.  

### What is matched ?


If I ask "thé" :
    It matches :
        "blabla bla,thé(200)." (a word, whatever stuck between non-letters)
        "blabla bla,THé(200)." (even with lower or upper case)
    It doesnt matches : 
        "blabla bla, théière (200)."  (no truncature on the right)
        "blabla bla, Pathé (200)."  (no troncature on the left)



"""

# Write the path to a copy (!!) of your Obsidian vault 
# ADVICE : don't run this code directly on your precious current vault
#          before you see what it can do to it! 
folder_path = "your/folder/path/here"




import os
import pandas as pd
import re
import yaml
import unicodedata






# Normalize tags: remove accents, keep only letters, and replace spaces with underscores
def normalize_tag(tag):
    # Remove accents by decomposing Unicode characters
    tag = unicodedata.normalize('NFKD', tag)
    tag = ''.join(c for c in tag if unicodedata.category(c) != 'Mn')  # Remove non-spacing marks (accents)
    # Keep only a-zA-Z and replace spaces with underscores
    tag = re.sub(r'[^a-zA-Z\s]', '', tag)
    tag = tag.replace(" ","_")
    # write tag in lowercase
    tag = tag.lower()
    return tag

# Load CSV into DataFrame
csv_path = "tags.csv"
tagdf = pd.read_csv(csv_path, names=["tag", "alias"])
tagdf["tag"] = tagdf["tag"].apply(normalize_tag)

# Write the updated DataFrame back to the CSV
tagdf.to_csv(csv_path, index=False, header=False, encoding="utf-8")
print("CSV file normalized successfully!")






def normalize_text(text):
    """
    Normalize a string, removing accents and going lower case.
    """
    # Transformer les caractères accentués en leur forme décomposée (ex. é → e + ´)
    normalized = unicodedata.normalize('NFD', text)
    # Supprimer les accents en ne gardant que les caractères ASCII
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn').lower()


def process_markdown_file(file_path):
    global tagdf

    # Load and process Markdown file
    markdown_path = file_path
    
    with open(markdown_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Separate YAML header and body
    yaml_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    
    # If YAML header is missing, create one
    if not yaml_match:
        print(f"YAML header missing in {markdown_path}, creating default header.")
        yaml_header = "---\ntags: []\n---"  # Default YAML header with an empty tags list
        markdown_body = content
    else:
        yaml_header = yaml_match.group(1)
        markdown_body = yaml_match.group(2)
    
   
    # Parse YAML header
    try:
        yaml_data = yaml.safe_load(yaml_header)
        if not isinstance(yaml_data, dict):
            yaml_data = {}  # Ensure it's a dictionary
    except yaml.YAMLError:
        yaml_data = {}  # Invalid YAML, set to empty dictionary

    # Ensure 'tags' key exists and is a list
    if "tags" not in yaml_data or not isinstance(yaml_data["tags"], list):
        yaml_data["tags"] = []
        
    # Search for aliases and update tags
    found_tags = set()
    for _, row in tagdf.iterrows():
        alias = row["alias"]
        
        # Skip non-string aliases (like NaN or None)
        if not isinstance(alias, str):
            continue
        
        # search the tag in the text as a single word
        # (improvement to do: dont look inside URL ?)
        alias_pattern = rf"\b{re.escape(alias)}\b"
        # to match the string wherever (truncature both sides)
        #alias_pattern = re.escape(alias)
        if re.search(alias_pattern.lower(), markdown_body.lower()):
            found_tags.add(row["tag"])
    
    # Update tags in YAML (avoid duplicates)
    yaml_data["tags"].extend(tag for tag in found_tags if tag not in yaml_data["tags"])

    # Generate updated YAML header with UTF-8 support for accented characters
    updated_yaml_header = yaml.dump(yaml_data, sort_keys=False, allow_unicode=True)
    
    # Reassemble Markdown file with updated YAML header
    updated_markdown_content = f"---\n{updated_yaml_header}---\n{markdown_body}"
    
    # Write the updated Markdown content back
    try:
        with open(markdown_path, "w", encoding="utf-8") as file:
            file.write(updated_markdown_content)
        print(".", end="")  # Progress indication
    except IOError as e:
        print(f"Error writing to {markdown_path}: {e}")



def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_markdown_file(os.path.join(root, file))
                print(".", end="")


process_folder(folder_path)



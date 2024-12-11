# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:29:11 2024

@author: pascaliensis, with ChatGPT 3.5

### Script Overview  

TL;DR: This script complements the `MarkdownTagUpdater.py` script by generating a `tags_a_trier.csv` file

- It scans the specified `folder_path` and its subfolders, opening all `.md` files (Obsidian notes).  
- For each note, it creates a `tag-alias` pair using the note's name as both the `tag` and the `alias`.  
- If the note contains aliases, it generates additional `tag-alias` pairs using the note's name as the `tag` and each alias as the `alias`.  
- If the note contails tags, they are collected in tag and alias
- Once inspected, the csv file needs to be renamed 'tags.csv'

Note: The script works with UTF-8 encoding.  

Important: The generated output requires thorough inspection, cleaning, and validation to ensure relevance. Consult your librarian for guidance on selecting appropriate tags.

"""


folder_path = "C:/Users\martinop\OneDrive - Universite de Montreal\perso\en_cours\myPython\pyObsidianUpdater"


import os
import pandas as pd
import re
import yaml

# Initialize an empty DataFrame for harvested data
harvest_df = pd.DataFrame(columns=["tag", "alias"])

def process_markdown_file(file_path):
    global harvest_df
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract filename without extension
    markdown_name = os.path.splitext(os.path.basename(file_path))[0]

    # Separate YAML header and body
    yaml_match = re.match(r"---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not yaml_match:
        return  # Skip if no YAML header

    yaml_header = yaml_match.group(1)

    # Parse YAML header
    try:
        yaml_data = yaml.safe_load(yaml_header)
        if not isinstance(yaml_data, dict):
            return  # Skip if YAML is not a dictionary
    except yaml.YAMLError:
        return  # Skip files with invalid YAML

    # Extract aliases if they exist
    aliases = yaml_data.get("aliases", [])
    if not isinstance(aliases, list):
        aliases = [aliases]
    
    # Extract tags if they exist
    tags = yaml_data.get("tags", [])
    if not isinstance(tags, list):
        tags = [tags]

    # Collect rows to add
    rows_to_add = [{"tag": markdown_name, "alias": markdown_name}]  # First row for file name
    rows_to_add.extend({"tag": markdown_name, "alias": alias} for alias in aliases)
    rows_to_add.extend({"tag": tag, "alias": tag} for tag in tags)

    # Concatenate new rows to the DataFrame
    harvest_df = pd.concat([harvest_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    # Remove duplicate rows based on the "alias" column
    harvest_df = harvest_df.drop_duplicates(subset='alias')

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                process_markdown_file(os.path.join(root, file))
                print(".", end="")


# Specify the folder to process
process_folder(folder_path)

# Save the harvested DataFrame to a CSV
harvest_csv_path = "tags_a_trier.csv"
harvest_df.to_csv(harvest_csv_path, index=False, encoding="utf-8")

print(f"\nHarvesting complete! Data saved to {harvest_csv_path}")
print("Please inspect carefully the output and rename it tags.csv")

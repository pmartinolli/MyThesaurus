# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:41:08 2024

@author: pascaliensis, with ChatGPT 3.5


Turn a 3 columns thesaurus from Thesaurus Builder in https://github.com/pmartinolli/MyThesaurus/tree/master/ThesaurusBuilder
     into a 2 columns thesaurus for re-indexing Obsidian or Zotero


"""

import pandas as pd
import numpy as np
import re

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame with specific columns.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the specified columns.
    """
    try:
        # Load the CSV file with the specified columns
        df = pd.read_csv(file_path, usecols=[
            "Generic_controlled_vocabulary", 
            "Specific_controlled_vocabulary", 
            "Aliases"
        ])
        print("CSV file loaded successfully.")
        return df
    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# Function to check if a string contains brackets and replace it
def remove_if_contains_brackets(cell):
    if isinstance(cell, str) and re.search(r'[\[\]\(\)\{\}]', cell):  # regex to find any brackets
        return np.nan  # or return "" to leave it as empty string
    return cell


# Function to remove everything after the "/"
def remove_after_slash(cell):
    if isinstance(cell, str):
        return cell.split('/')[0]  # Keep everything before the first "/"
    return cell







# Replace 'path_to_your_file.csv' with the actual file path
file_path = "TTRPG_thesaurus.csv"
df = load_csv(file_path)




df_temp1 = df
df_temp1 = df_temp1.drop('Aliases', axis=1)
df_temp1 = df_temp1.rename(columns={'Generic_controlled_vocabulary': 'tag',
                                    'Specific_controlled_vocabulary' : 'alias' })
# remove rows where cells are empty
df_temp1 = df_temp1.dropna()




df_temp2 = df
df_temp2 = df_temp2.drop('Generic_controlled_vocabulary', axis=1)
df_temp2 = df_temp2.drop('Aliases', axis=1)
df_temp2['Specific_controlled_vocabulary2'] = df_temp2['Specific_controlled_vocabulary'] 
df_temp2 = df_temp2.rename(columns={'Specific_controlled_vocabulary': 'tag',
                                    'Specific_controlled_vocabulary2' : 'alias'})
# remove rows where cells are empty
df_temp2 = df_temp2.dropna()
# Remove leading underscores from the 'alias' column
df_temp2['alias'] = df_temp2['alias'].str.lstrip('_')




df_temp3 = df
df_temp3 = df_temp3.drop('Generic_controlled_vocabulary', axis=1)
df_temp3 = df_temp3.rename(columns={'Specific_controlled_vocabulary': 'tag',
                                    'Aliases' : 'alias'})
# Assuming `df` is your DataFrame with columns 'tag' and 'alias'
df_expanded = df_temp3.dropna(subset=["alias"]).copy()  # Remove rows with NaN in 'alias'
df_expanded["alias"] = df_expanded["alias"].str.split(";")  # Split strings by ';'
df_temp3 = df_expanded.explode("alias").reset_index(drop=True)  # Expand into new rows
# remove rows where cells are empty
df_temp3 = df_temp3.dropna()

# Assuming dfs are your DataFrames with the same structure
combined_df = pd.concat([df_temp1, df_temp2, df_temp3], ignore_index=True)

# Trim leading and trailing spaces from all cells in the DataFrame
combined_df = combined_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Remove cells with brackets [] () {}
combined_df = combined_df.applymap(remove_if_contains_brackets)

# Remove text after "/"
combined_df = combined_df.applymap(remove_after_slash)

# Replace empty strings with NaN and then drop rows with NaN values
combined_df = combined_df.replace('', pd.NA).dropna()




# Write DataFrame to CSV
combined_df.to_csv('tags_a_trier.csv', index=False)
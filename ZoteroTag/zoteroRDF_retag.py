# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:35:09 2024

@author: pascaliensis, with ChatGPT 3.5 et Claude 

This code takes an export of Zotero (Bibliontology RDF or Zotero RDF)
    And it automatically adds tags based on a two columns CSV "tags.csv"
        The keywords are searched in titles, keywords, abstracts
And it writes another *_retag.rdf with these news tags inside



Some bugs remaining for very large and complex libraries of references 
(Zotero will not accept the _retag back)


"""

import csv
import re



# Put the name of your RDF Zotero export file here
# In the same folder with this Python script


filename = 'testBIBO.rdf'

filename = 'test.rdf'
filename = 'wargamingEssaysBIBO.rdf'

filename = 'academicTTRPG.rdf'

filename = 'Teilhard de Chardin in Science Fiction_BIBO_retag.rdf'




### Extract the potential tags in the pseudo XML of RDF file

def extract_subtag(filename, pretag):
    
    """
    Extract words following '    <pretag:' at the start of lines in a text file.

    Args:
        filename (str): Path to the text file to be processed
        pretag (str): name of the tag

    Returns:
        list: Words extracted from lines starting with '    <pretag:'
    """
    
    extracted_words = []

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            
            for line in file:
                
                if pretag == "ctag" : # THREE spaces 
                    # Strip whitespace and check if line starts with '   <pretag:'
                    if line.startswith(f'   <{pretag}:'):
                        # Attempt to split the line and validate the result
                        parts = line.strip().split(f'<{pretag}:')
                        if len(parts) > 1:
                            word = parts[1].split(' ')[0]  # Get the first part after the split
                            word = f'{pretag}:{word}'
                            extracted_words.append(word)     
                        break
                else : 
                    # Strip whitespace and check if line starts with '    <pretag:'
                    if line.startswith(f'    <{pretag}:'):
                        # Attempt to split the line and validate the result
                        parts = line.strip().split(f'<{pretag}:')
                        if len(parts) > 1:
                            word = parts[1].split(' ')[0]  # Get the first part after the split
                            word = f'{pretag}:{word}'
                            extracted_words.append(word)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove duplicates
    extracted_document_types = list(dict.fromkeys(extracted_words))
    return extracted_document_types

    




# Extract groups of tags (and for bib and bibo, add news tags)

def process_chunks(filename, rdf_tag, tagtype_list):
    """
    Args:
        filename (str): Path to the text file to be processed
        rdf_tag (str)
        tagtype_list (list): List of types of tags

    Returns:
        list: Extracted and modified chunks 
    """
    
    
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            # Read entire file content
            content = file.read()
                          
            # Split the content into lines
            lines = content.splitlines()
            chunks = []
            
            # Iterate through lines
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check if line starts with any of the desired opening tags
                for tagtype in tagtype_list:
                    
                    start_tag = f'    <{tagtype} '
                    end_tag = f'    </{tagtype}>'    
        
                    if line.startswith(start_tag):
                        # Create a chunk from this line
                        chunk = []
                        chunk.append(line)
                        i += 1
        
                        # Collect all lines until the closing tag is found
                        while i < len(lines) and not lines[i].startswith(end_tag):
                            chunk.append(lines[i])
                            i += 1
        
                        # Include the closing tag
                        if i < len(lines):
                            chunk.append(lines[i])

                        # turn chunk (list of strings) into a string
                        chunck_string = "\n".join(chunk)
                        
                        # process the chunck_string here
                        if rdf_tag == "bibo" : 
               
                            # Extract all strings between <dd> and </dd>
                            dctitle_list = re.findall(r'<dcterms:title>(.*?)</dcterms:title>', chunck_string, re.DOTALL)
                            dctitles = '\n'.join(dctitle_list)
                            
                            dcabstract_list = re.findall(r'<dcterms:abstract>(.*?)</dcterms:abstract>', chunck_string, re.DOTALL)
                            dcabstracts = '\n'.join(dcabstract_list)
                            
                            dcsubject_list = re.findall(r'<ctag:label>(.*?)</ctag:label>', chunck_string, re.DOTALL)
                            # cleaning the automatic tags 
                            dcsubjects = '\n'.join(dcsubject_list)
                            dcsubjects = re.sub(r'<ctag:tagged>', '', dcsubjects)
                            dcsubjects = re.sub(r'</ctag:label>', '', dcsubjects)
                            
                            searching_zone = dctitles + "\n" + dcabstracts + "\n" + dcsubjects
                            #print(searching_zone)
                            
                            # position1: Match aliases and append corresponding tags
                            list_of_potential_insertion = []
                            
                            # First turn
                            for thesaurus_tag in thesaurus_tags_list:
                                # extract keyword for searching it in searching_zone
                                keyword = thesaurus_tag['alias']  
                                # preparing the part to include
                                potential_insertion = f'<ctag:label>{thesaurus_tag["tag"]}</ctag:label>'
                                if keyword.lower() in searching_zone.lower() and potential_insertion not in chunck_string :
                                    list_of_potential_insertion.append(potential_insertion)

                            # Second turn (in case there is a two-level thesaurus)
                            # This turn will produce generic tags from specific tags (produced in first turn)
                            for thesaurus_tag in thesaurus_tags_list:
                                # extract keyword for searching it in searching_zone
                                keyword = thesaurus_tag['alias']  
                                # preparing the part to include
                                potential_insertion = f'<ctag:label>{thesaurus_tag["tag"]}</ctag:label>'
                                if keyword.lower() in searching_zone.lower() and potential_insertion not in chunck_string :
                                    list_of_potential_insertion.append(potential_insertion)

                                
                            if len(list_of_potential_insertion) > 0:

                                # removing duplicate lines of tags
                                list_of_potential_insertion = list(dict.fromkeys(list_of_potential_insertion))
                                
                                labels_2insert = "\n                ".join(list_of_potential_insertion)
                                before_labels = "        <ctag:tagged>\n            <ctag:UserTag>\n                "
                                after_labels = "\n            </ctag:UserTag>\n        </ctag:tagged>\n"

                                insertion_point = chunck_string.rfind(end_tag)
                                chunck_string = (
                                    chunck_string[:insertion_point]
                                    + before_labels
                                    + labels_2insert
                                    + after_labels
                                    + chunck_string[insertion_point:]
                                )




                                
                        # process the chunck_string here
                        if rdf_tag == "bib" : 
               
                            # Extract all strings between <dd> and </dd>
                            dctitle_list = re.findall(r'<dc:title>(.*?)</dc:title>', chunck_string, re.DOTALL)
                            dctitles = '\n'.join(dctitle_list)
                            
                            dcabstract_list = re.findall(r'<dcterms:abstract>(.*?)</dcterms:abstract>', chunck_string, re.DOTALL)
                            dcabstracts = '\n'.join(dcabstract_list)
                            
                            dcsubject_list = re.findall(r'<dc:subject>(.*?)</dc:subject>', chunck_string, re.DOTALL)
                            # cleaning the automatic tags 
                            dcsubjects = '\n'.join(dcsubject_list)
                            dcsubjects = re.sub(r'<z:AutomaticTag><rdf:value>', '', dcsubjects)
                            dcsubjects = re.sub(r'</rdf:value></z:AutomaticTag>', '', dcsubjects)
                            
                            searching_zone = dctitles + "\n" + dcabstracts + "\n" + dcsubjects
                            #print(searching_zone)
                            
                            # first turn 
                            for thesaurus_tag in thesaurus_tags_list:
                                keyword = thesaurus_tag['alias']  
                                potential_insertion = f'        <dc:subject>{thesaurus_tag["tag"]}</dc:subject>\n'
                                if keyword.lower() in searching_zone.lower() and potential_insertion not in chunck_string :
                                        insertion_point = chunck_string.rfind(end_tag)
                                        chunck_string = (
                                            chunck_string[:insertion_point]
                                            + potential_insertion
                                            + chunck_string[insertion_point:]
                                        )

                            # second turn, to incorporate generic tags (based on specific tags just produced in first turn )
                            # in case of two-levels thesaurus 
                            for thesaurus_tag in thesaurus_tags_list:
                                keyword = thesaurus_tag['alias']  
                                potential_insertion = f'        <dc:subject>{thesaurus_tag["tag"]}</dc:subject>\n'
                                if keyword.lower() in searching_zone.lower() and potential_insertion not in chunck_string :
                                        insertion_point = chunck_string.rfind(end_tag)
                                        chunck_string = (
                                            chunck_string[:insertion_point]
                                            + potential_insertion
                                            + chunck_string[insertion_point:]
                                        )

                        chunks.append(chunck_string)
                        break
        
                i += 1

        return chunks
                       
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    





def process_ctags(filename):
    """
    Extracts lines starting with ctag 

    Args:
        filename (str): Path to the text file to be processed

    Returns:
        list: Extracted lines starting with 3 SPACES + ctag tag
    """
    chunks = []

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            # Read all lines from the file
            lines = file.readlines()

            # Define the start tag to look for
            start_tag = '   <ctag:UserTag '

            # Iterate through lines to find matching ones
            for line in lines:
                if line.startswith(start_tag):
                    chunks.append(line)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return chunks




################################################################################

### MAIN SCRIPT


# Import the thesaurus tags.csv

thesaurus_filename = 'tags.csv'

try:
    # Read the thesaurus_tags file into a list of dictionaries
    thesaurus_tags_list = []
    with open(thesaurus_filename, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            thesaurus_tags_list.append(row)
except FileNotFoundError:
    print("Error: Thesaurus 'tags.csv' not found.")
except Exception as e:
    print(f"An error occurred: {e}")







extracted_bibo_types = extract_subtag(filename, "bibo")
extracted_z_types = extract_subtag(filename, "z")
extracted_foaf_types = extract_subtag(filename, "foaf")
extracted_ctag_types = extract_subtag(filename, "ctag")

extracted_bib_types = extract_subtag(filename, "bib")
extracted_rdf_types = extract_subtag(filename, "rdf")



all_the_bibos = process_chunks(filename, "bibo", extracted_bibo_types)
all_the_zeds = process_chunks(filename, "z", extracted_z_types)
all_the_foafs = process_chunks(filename, "foaf", extracted_foaf_types)
all_the_ctags = process_ctags(filename)

all_the_bibs = process_chunks(filename, "bib", extracted_bib_types)
all_the_rdfs = process_chunks(filename, "rdf", extracted_rdf_types)









# Header of the Zotero RDF Export file

if all_the_bibs is not None and len(all_the_bibs) > 0:
    rebuilt_rdf = """<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:z="http://www.zotero.org/namespaces/export#"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:vcard="http://nwalsh.com/rdf/vCard#"
 xmlns:foaf="http://xmlns.com/foaf/0.1/"
 xmlns:bib="http://purl.org/net/biblio#"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:prism="http://prismstandard.org/namespaces/1.2/basic/"
 xmlns:link="http://purl.org/rss/1.0/modules/link/">\n"""
    pass

else : 
    rebuilt_rdf = """<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:res="http://purl.org/vocab/resourcelist/schema#"
 xmlns:z="http://www.zotero.org/namespaces/export#"
 xmlns:bibo="http://purl.org/ontology/bibo/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:foaf="http://xmlns.com/foaf/0.1/"
 xmlns:ctag="http://commontag.org/ns#"
 xmlns:address="http://schemas.talis.com/2005/address/schema#"
 xmlns:sioct="http://rdfs.org/sioc/types#"
 xmlns:po="http://purl.org/ontology/po/"
 xmlns:sc="http://umbel.org/umbel/sc/">\n"""
         
     




# Add each extracted chunk
if all_the_bibos is not None and len(all_the_bibos) > 0:
    for bibo in all_the_bibos:
         rebuilt_rdf = rebuilt_rdf + bibo + "\n"


if all_the_bibs is not None and len(all_the_bibs) > 0: 
    for bibi in all_the_bibs:
        rebuilt_rdf = rebuilt_rdf + bibi + "\n"   

if all_the_rdfs is not None and len(all_the_rdfs) > 0: 
    for rdfi in all_the_rdfs:
        rebuilt_rdf = rebuilt_rdf + rdfi + "\n"     
     
if all_the_zeds is not None and len(all_the_zeds) > 0:       
    for zee in all_the_zeds:
          rebuilt_rdf = rebuilt_rdf + zee + "\n"  

if all_the_foafs is not None and len(all_the_foafs) > 0:        
    for foafi in all_the_foafs:
          rebuilt_rdf = rebuilt_rdf + foafi + "\n" 

if all_the_ctags is not None and len(all_the_ctags) > 0: 
    for ctagi in all_the_ctags:
          rebuilt_rdf = rebuilt_rdf + ctagi           
       

# final tag of the Zotero RDF Export file   
rebuilt_rdf = rebuilt_rdf + "</rdf:RDF>\n"






# write another RDF file to import back in Zotero with all new shiny tags

retag_filename = filename.rsplit('.', 1)[0]  # Remove file extension
retag_filename = f"{retag_filename}_retag.rdf"


with open(retag_filename, 'w', encoding="utf-8") as file:
    # Write the rebuilt RDF file
    file.write(rebuilt_rdf)


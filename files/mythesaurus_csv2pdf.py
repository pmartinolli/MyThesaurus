# -*- coding: utf-8 -*-


"""
Created in November 2024

@author: Pascaliensis, with ChatGPT3.5 

This code takes a CSV file and turn it into a prety PDF in 4 columns, 
displaying two-levels controlled vocabulary and its aliases

"""

import pandas as pd


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.units import mm
from reportlab.lib import colors


# Load CSV data
csv_file = "TTRPG_thesaurus.csv"  # replace with your CSV file name
data = pd.read_csv(csv_file)


# After processing all grouped_data paragraphs, add the final paragraph
final_text = "_[rpgname]_game \n_[countryname]_country\n\ngenerated from csv with https://github.com/pmartinolli/MyThesaurus/blob/master/files/mythesaurus_csv2pdf.py"



# Define styles for the PDF content
generic_style = ParagraphStyle(
    "GenericStyle",
    fontSize=8,
    leading=10,
    textColor=colors.black,
    fontName="Helvetica-Bold",
)

combined_style = ParagraphStyle(
    "CombinedStyle",
    fontSize=7,
    leading=8,
    textColor=colors.black,
    fontName="Helvetica",
    allowHtml=True  # Enable HTML-like tags for styling
)

# Create a PDF document with reduced margins
pdf_filename = "TTRPG_thesaurus.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    topMargin=15 * mm,  # Reduced top margin
    bottomMargin=15 * mm  # Reduced bottom margin
)
width, height = letter

# Define four frames for four columns
frame_width = width / 4 - 10 * mm  # Subtract a small margin for spacing
frames = [
    Frame(10 * mm + i * (frame_width + 5 * mm), 15 * mm, frame_width, height - 30 * mm)
    for i in range(4)
]

# Assign the frames to the page template
page_template = PageTemplate(frames=frames)
doc.addPageTemplates(page_template)

# Gather content to add to the frames
elements = []

# Sort data by "Generic_controlled_vocabulary" in descending order and group
sorted_data = data.sort_values("Generic_controlled_vocabulary", ascending=False)
grouped_data = sorted_data.groupby("Generic_controlled_vocabulary", sort=False)

# Iterate over the sorted and grouped data
for generic_value, group in grouped_data:
    # Add the generic value in bold size 9
    # elements.append(Paragraph(generic_value, generic_style))
    
    # Check if there's any non-null Alias in the group
    alias_text = str(grouped_data['Aliases'])
    
    if alias_text:  # If there's an alias associated with the generic value
        # Format with generic_value and associated alias
        combined_text = f"<b>{generic_value}</b> <font size=7 color='gray'>{alias_text}</font>"
        combined_paragraph = Paragraph(combined_text, combined_style)
        elements.append(combined_paragraph)
    else:
        # Add the generic value alone in bold size 9 if no alias is found
        elements.append(Paragraph(generic_value, generic_style))
    
    elements.append(Spacer(1, 2))  # Add a line break

    # Sort the group by "Specific_controlled_vocabulary" in ascending order
    sorted_group = group.sort_values("Specific_controlled_vocabulary", ascending=True)
    # Add each specific value along with its aliases
    for _, row in sorted_group.iterrows():
        
        specific_text = str(row['Specific_controlled_vocabulary']) if isinstance(row['Specific_controlled_vocabulary'], str) else ""
        
        if specific_text != "" : 
            alias_text = str(row['Aliases']) if isinstance(row['Aliases'], str) else ""
            # add ":" if there is an alias 
            if alias_text != "" : 
                specific_text = specific_text + ":"
            
        # Combine specific text and alias text with HTML-style tags
        combined_text = f"<b>{specific_text}</b> <font size=6 color='gray'>{alias_text}</font>"
        combined_paragraph = Paragraph(combined_text, combined_style)
        
        elements.append(combined_paragraph)

    elements.append(Spacer(1, 8))  # Add two line breaks before next block
    
# Add the final text
elements.append(Paragraph(final_text, combined_style))

# Build the document with flowing text in columns
doc.build(elements)

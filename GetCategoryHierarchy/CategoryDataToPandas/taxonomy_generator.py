import pandas as pd
import os
from typing import List
import json
from taxonomy_dataclasses import (
    CategoryHierarchy, AreaCategory, BroadCategory, MajorCategory, DetailedCategory
)

# Get the directory of the current script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the data directory relative to the current script directory
DATA_DIR = os.path.join(SCRIPT_DIR, "../data/ncsesTaxonomy")

# Define the JSON output directory relative to the current script directory
JSON_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../data/taxonomyJson")

# Function to read Excel files from a directory and convert them to a single DataFrame
def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df

def get_ncses_taxonomy_data(data_dir):
    # Collect all spreadsheet files in the data directory to account for if we add more data
    all_data = []
    for file in os.listdir(data_dir):
        if file.endswith('.xlsx'):
            file_path = os.path.join(data_dir, file)
            df = read_excel_file(file_path)
            all_data.append(df)
    return all_data

def get_ncses_taxonomy_data_as_df(data_dir):
    all_data = get_ncses_taxonomy_data(data_dir)
    return pd.concat(all_data, ignore_index=True)

def construct_category_hierarchy(df):
    # Initialize the category hierarchy
    area_categories = []
    
    current_area = None
    current_broad = None
    current_major = None
    
    # Iterate through the DataFrame to build the hierarchy
    for i, row in df.iterrows():
        # Check if the row is a new area category
        if row['Unnamed: 1'] == 'Area':
            # Create a new AreaCategory and reset the current broad and major categories
            current_area = AreaCategory(name=row['Table 4'], broad_categories=[])
            area_categories.append(current_area)
        
        # Check if the row is a new broad category
        elif row['Unnamed: 1'] == 'Broad':
            # Create a new BroadCategory and reset the current major category
            current_broad = BroadCategory(name=row['Table 4'], inner_categories=[])
            current_area.broad_categories.append(current_broad)
        
        # Check if the row is a new major category
        elif row['Unnamed: 1'] == 'Major':
            # Create a new MajorCategory and reset the current detailed category
            current_major = MajorCategory(name=row['Table 4'], detailed_categories=[])
            current_broad.inner_categories.append(current_major)
        
        elif row['Unnamed: 1'] == 'Detailed':
            # Create a new DetailedCategory
            detailed_category = DetailedCategory(name=row['Table 4'])
            current_major.detailed_categories.append(detailed_category)
    
    # Create a final CategoryHierarchy object
    category_hierarchy = CategoryHierarchy(area_categories=area_categories)
    return category_hierarchy

def print_pandas_structure(df):
    # Set pandas display options for better readability
    pd.set_option('display.max_rows', 10)  # Limit the number of rows displayed
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', 1000)  # Set the display width to avoid line breaks
    pd.set_option('display.max_colwidth', 50)  # Limit the width of each column
    pd.set_option('display.float_format', '{:.2f}'.format)  # Format floats to 2 decimal places

    print("DataFrame Head:")
    print(df.head())  # Print the first few rows of the DataFrame
    print("\nColumns:")
    print(df.columns)  # Print the column names
    print("\nIndex:")
    print(df.index)  # Print the index
    print("\nData Types:")
    print(df.dtypes)  # Print the data types of each column
    print("\nShape:")
    print(df.shape)  # Print the shape of the DataFrame
    print("\nInfo:")
    print(df.info())  # Print concise summary of the DataFrame
    print("\nDescribe:")
    print(df.describe(include='all'))  # Print summary statistics for all columns

df = get_ncses_taxonomy_data_as_df(DATA_DIR)
# Uncomment to print the pandas structure of the dataframe along with a few other details
# print_pandas_structure(df)
category_hierarchy = construct_category_hierarchy(df)

json_file_path = os.path.join(JSON_OUTPUT_DIR, 'taxonomy_hierarchy.json')

# Save the JSON data to a file
# the .to_dict() method is used to convert the dataclass object to a dictionary
# each to_dict() call will cascade through the dataclass and convert each nested dataclass to a dictionary
# this will continue until all nested dataclasses are converted to dictionaries
# the resulting dictionary can then be converted to JSON
with open(json_file_path, 'w') as json_file:
    json.dump(category_hierarchy.to_dict(), json_file, indent=4)

print(f"JSON data has been saved to {json_file_path}")

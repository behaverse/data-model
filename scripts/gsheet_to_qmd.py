

import shutil
import os
import pandas as pd


## Get access to the google spreadsheet
sheet_id = "1LWTXsg2T4NPo0xbhD4pulIgkEJk5Oey7FusItltlCk8"
main_sheet = "Tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={main_sheet}"

output_dir = '../auto-generated/'





# helper function to load a specific sheet in the gsheet
def load_table(table_name):
    url_table = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={table_name}"
    return pd.read_csv(url_table)


def print_header(df_row):
    """
    Generates the header text for the documentation file.
    """
    
    
    # extract data from df
    table_name = df_row.iloc[0]['table_name']
    table_description = df_row.iloc[0]['table_description']
    #nav_order = df_row.iloc[0]['nav_order']
    #table_level = df_row.iloc[0]['table_level']
    #parent = df_row.iloc[0]['parent']
    #grand_parent = df_row.iloc[0]['grand_parent']
   
    
    
    # format string
    header = f"\n# {table_name} Table\n\n {table_description}\n\n<br>"
    return header





def print_row(row):
    """Generates a chunk of text describing a specific row of the codebook.

    Args:
        row (pd.DataFrame): A row of the codebook dataframe.
    """

    name = f'{row["name"]}\t[{row["data_type"]}]\n'
    description = f': {row["description"]}\n'
    
    
    if not pd.isna(row['index_scope']):
        index_scope = f': {row["index_scope"]}\n'
    else:
        index_scope = ''
    
    
    # for enum variables need to print out possible values
    # we also have section headers (e.g., "context") which should only be printed if they change
    # across row
    #if row['data_type'] == 'enum':
    if not pd.isna(row['enum_values']):    
        enum_text = enum2text(row)
    else:
        enum_text = ''
    
    # There can be up to 3 notes for each codebook entry
    notes = [f'\n:::{{.callout-note}}\n\n {row["note_" + str(i)]} \n\n:::\n' for i in range(1,4) if not pd.isna(row["note_" + str(i)])]
    notes = '\n'.join(notes)
 
    output = name + description + index_scope + enum_text + notes + '\n\n\n'
    
    return(output)




def enum2text(row):
    """Converts data describing an enum in the codebook (formatted as json) in a md formatted string. 

    Args:
        row (pd.DataFrame): A row of the codebook dataframe.
    """
    if pd.isna(row['enum_values']):
        enum_text = ''
    else: 
        enum_df = pd.read_json(row['enum_values'], orient = 'index')
        enum_text = enum_df.apply(lambda rr: f':  **{rr["name"]}:** {rr["description"]}', axis = 1)
        enum_text = '\n'.join(enum_text) + '\n'
                                
    return(enum_text)




def print_table(df):
    old_category = ''
    md_text = ''

    for idx, row in df.iterrows():
    
        # get header title for group of variables
        current_category = row['category']
        if not pd.isna(current_category):
            if current_category != old_category:
                old_category = current_category
                category_header = "\n\n## " + current_category + "\n\n"
                md_text += category_header

        # convert and concatenate each row    
        md_text += print_row(row)
    
    return md_text





def save_qmd(content, filename):
    # write documentation into qmd file
    md_file = open(filename + '.qmd', 'w')
    md_file.write(content)
    md_file.close()





def generate_qmd():

    # Delete all content from auto-generated
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # load data
    tables = pd.read_csv(url)
    table_count = len(tables["table_name"])


    for current_table_index in range(table_count): # loop over tables

        # create header for this table using info from the "Tables" sheet
        header_txt = print_header(tables.iloc[[current_table_index]])

        # create body for this table
        # -- load sheet for this table
        current_table_name = tables["table_name"][current_table_index]
        print(f"Processing Table: {current_table_name}")
        df = load_table(current_table_name)
        
        # format content of the sheet
        body_txt = print_table(df)

        # write to file
        save_qmd(content=header_txt + body_txt, 
                filename=output_dir + current_table_name)




if __name__ == '__main__':
    generate_qmd()


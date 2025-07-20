# Convert "bdm_trial_spec_v2" from Google Sheets to Quarto YAML and QMD files
# use: uv run --env-file .env python scripts/gsheets_to_quarto.py

# Imports and setup

import re
import os
from pathlib import Path
import pandas as pd
import yaml
import requests

# Parameters

TRIAL_SPEC_SHEET_ID = os.environ['TRIAL_SPEC_SHEET_ID']  # Google Sheet ID for the trial specifications
OUTPUT_DIR = Path('assets/auto-generated/')  # where to write the generated files
QMD_OUTPUT_DIR = Path('spec/')

if OUTPUT_DIR.exists() and not (OUTPUT_DIR / '.lock').exists():
    print('The output directory is manually edited.'
          'Skipping auto-generation.')
    exit(1)

# Helper functions

def camel_to_dash(camel_case_string):
  """Converts a CamelCase string to a dash-separated lower case string.

  Args:
    camel_case_string: The CamelCase string to convert.

  Returns:
    The dash-separated lower-case string.
  """
  import re

  if pd.isna(camel_case_string):
    raise ValueError('camel_case_string cannot be None')

  if camel_case_string.strip() == '':
    return camel_case_string.strip()

  # replace spaces with empty string, and prefix uppercase letters with a dash
  s = re.sub('(?!^)([A-Z]+)', r'-\1', camel_case_string.replace(' ', ''))
  return s.lower()

def get_sheet(sheet_id: str, sheet_name, backend: str='requests'):
    """Downloads a Google sheet as a pandas DataFrame."""
    url = 'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'.format(
        sheet_id=sheet_id, sheet_name=sheet_name
    )

    if backend.lower() == 'requests':
      from io import StringIO
      content = requests.get(url).content
      data = pd.read_csv(StringIO(content.decode('utf-8')))
    else:
      data = pd.read_csv(url)
    return data

def convert_sheet_to_yaml(table_info: pd.Series, root_dir) -> Path:
    """Write a pandas DataFrame to a CSV file."""

    assert table_info['name'] is not None, 'table name is required'

    file_name = camel_to_dash(table_info['name']) + '.yml'
    output_path = root_dir / file_name

    # if category exists, append it to the file path
    if (pd.notna(table_info['category']) and len(table_info['category']) > 0):
      category = camel_to_dash(table_info['category'])
      output_path = root_dir / category / file_name

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = get_sheet(TRIAL_SPEC_SHEET_ID, table_info['name'])

    with open(output_path, 'w') as f:

      # reformat to match quarto listing's `categories` field
      if 'category' in df.columns:
        df.rename(columns={'category': 'categories'}, inplace=True)
        df['categories'] = df['categories'].apply(
          lambda cats: cats.split(';') if pd.notna(cats) else [])

      df['description'] = df['description'].fillna('')

      # handle %TABLE% annotations
      df = df.apply(lambda col: col.map(lambda x:
        re.sub(r'%([^%\s]+)%', r'<b><i class="bi bi-grid-3x3"></i> \1</b>', x)
        if isinstance(x, str) else x))

      df['notes'] = df['notes'].apply(lambda x:
        x.split('\n\n') if pd.notna(x) else None)

      # convert to a list of dictionaries
      items = df.to_dict(orient='records')

      # recursively drop nan values from the items
      for item in items:
        keys_to_delete = [key for key in item.keys()
                          if not isinstance(item[key], list)
                             and pd.isna(item[key])]
        for key in keys_to_delete:
          del item[key]

      # write to YAML
      yaml.safe_dump(
        items,
        f, indent=2, sort_keys=False)

    return output_path


# running the trials-gsheet-to-yaml pipeline

(OUTPUT_DIR / 'trials').mkdir(parents=True, exist_ok=True)

tables = get_sheet(TRIAL_SPEC_SHEET_ID, 'Tables')
tables.reset_index(drop=False, inplace=True)

# write the tables metadata to trials/tables.csv
with open(OUTPUT_DIR / 'trials/tables.yml', 'w') as f:
    tables_dict = tables.to_dict(orient='records')
    yaml.safe_dump(tables_dict, f, indent=2, sort_keys=False)


tables = tables.query('publish == True')
tables['category'] = tables['category'].str.split('; ')
tables = tables.explode('category').reset_index(drop=True)

with open(OUTPUT_DIR / '.lock', 'w') as f:
    f.write('WARNING:\n'
            'THIS FOLDER CONTAINS AUTO-GENERATED CONTENTS.\n'
            'EITHER DO NOT MANUALLY EDIT ITS CONTENT OR\n'
            'REMOVE THIS FILE TO DISABLE AUTO-GENERATION.')

tables.apply(convert_sheet_to_yaml, axis=1, root_dir=OUTPUT_DIR)


trials_index_template = \
"""
---
title: <i class="bi bi-database"></i> Trials data
subtitle: Trials are the main features of the scientific experiment
toc: false
listing:
  id: trial-tables-listing
  template: ../../assets/templates/trial-tables-listing.ejs
  sort: "order"
  categories: false
  filter-ui: false
  sort-ui: false
  contents:
    - "*.qmd"
---

A trial is a single instance of a participant interacting with a task. It contains information about the participant, the task, and the interaction between the two. BDM supports multiple trial-related tables that are designed to be as flexible as possible, allowing for a wide range of cognitive tasks to be represented.

::: {.callout-tip appearance="simple"}
We use <i class="bi bi-grid-3x3"></i> icon to refer to specific tables. For example the **<i class="bi bi-grid-3x3"></i> Response** table or the **<i class="bi bi-grid-3x3"></i> Stimulus** table.
:::

::: {#trial-tables-listing}
:::

"""

qmd_template = \
"""---
title: '<i class="bi bi-grid-3x3"></i> {title}'
output-file: {output_file}
subtitle: "{subtitle}"
order: {order}
toc: false
listing: 
  template: {ejs_template_path}
  field-required: [variable_name, categories, description]
  filter-ui: true
  sort: false
  sort-ui: false
  categories: numbered
  page-size: 10000
  contents:
    - "{yml_path}"
---

"""

tables_df = pd.DataFrame(
    yaml.safe_load(open('assets/auto-generated/trials/tables.yml'))
)
tables_df.set_index('name', inplace=True)

for yml_file in Path(OUTPUT_DIR).rglob('*.yml'):
    if yml_file.name == 'tables.yml':
        continue

    category = yml_file.parent.name
    category = None if category == 'auto-generated' else category

    # e.g., 'stimulus-component' -> 'StimulusComponent'
    table_name: str = yml_file.stem.title().replace('-', '')
    table_title: str = str(tables_df.loc[table_name, 'label'])
    table_description: str = str(tables_df.loc[table_name, 'description'])
    table_order: int = int(tables_df.loc[table_name, 'index']) + 1

    if category is None:
        continue

    _category_dir = QMD_OUTPUT_DIR / category
    qmd_file = _category_dir / (str(table_order) + '-' + yml_file.with_suffix('.qmd').name)
    qmd_file.parent.mkdir(parents=True, exist_ok=True)

    template_file = Path(f'assets/templates/{category}.ejs').relative_to(qmd_file.parent, walk_up=True)

    if _category_dir.exists() and \
        not (_category_dir / '.lock').exists():
        raise Exception('The qmd directory has been manually edited. Skipping auto-generation.')

    # Write a warning file
    with open(_category_dir / '.lock', 'w') as f:
        f.write('WARNING:\n'
                'THIS FOLDER CONTAINS AUTO-GENERATED CONTENTS.\n'
                'EITHER DO NOT MANUALLY EDIT ITS CONTENT OR\n'
                'REMOVE THIS FILE TO DISABLE AUTO-GENERATION.')

    print(f'Processing {qmd_file} in {category} category...')

    if not _category_dir.exists():
        _category_dir.mkdir(parents=True, exist_ok=True)


    qmd_content = qmd_template.format(
        title=table_title,
        subtitle=table_description,
        output_file=qmd_file.stem.partition('-')[2],
        order=table_order,
        ejs_template_path=template_file,
        yml_path=yml_file.relative_to(qmd_file.parent, walk_up=True)
    )

    with open(qmd_file, 'w') as f:
        f.write(qmd_content)

print("Writing trials index file...")
# TODO use _category_dir to identify the category index file
trials_index_file = QMD_OUTPUT_DIR / "trials" / "index.qmd"
trials_index_file.parent.mkdir(parents=True, exist_ok=True)
with open(trials_index_file, 'w') as f:
    f.write(trials_index_template)

print('Done!')
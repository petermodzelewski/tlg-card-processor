import pandas as pd
from jinja2 import Template


def create_template(filename: str):
    with open(filename, encoding='utf-8') as template:
        html_template = template.read()
    return Template(html_template)


def build_synonyms(category: str):
    export_data = pd.read_csv('data/export.csv', usecols=["Title", "Categories", "Synonyms"], keep_default_na=False)
    cards = export_data[export_data['Categories'] == category]
    synonyms = {}
    for index, row in cards.iterrows():
        synonyms[row['Title']] = row['Synonyms'].split(',')
    return synonyms
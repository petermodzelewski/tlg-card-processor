import json
import re
import os
import time
import pandas as pd
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from jinja2 import Template
from pathlib import Path

version = int(round(time.time() * 1000))
Path("result/lor").mkdir(parents=True, exist_ok=True)

@dataclass_json
@dataclass
class CardData:
    name: str
    cardCode: str


def create_template(filename: str):
    with open(filename, encoding='utf-8') as template:
        html_template = template.read()
    return Template(html_template)


glossary_template = create_template("data/lor/lor_card_glossary.html")
csv_row_template = create_template("data/csv_row.csv")


def add_csv_line(card, file, current_synonyms: list):
    glossary_html = glossary_template.render(version=version, card=card)
    description = glossary_html.replace("\"", "\"\"")
    if "'" in card.name:
        synonyms = card.name.replace("'", "")
        if synonyms not in current_synonyms:
            current_synonyms.append(synonyms)
    new_synonyms = ",".join(current_synonyms)
    category = "lor_card"
    glossary = csv_row_template.render(card_name=card.name, description=description, synonyms=new_synonyms, category=category)
    file.write(f"{glossary}\n")


if __name__ == '__main__':
    result_file = open('result/lor/lor-import.csv', 'w', encoding='utf-8')
    result_file.write('"Id","Title","Excerpt","Description","Synonyms","Variations","Categories"\n')

    with open('data/lor/cards.json', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    d = json.loads(data)
    for card_data in d:
        card = CardData.from_dict(card_data)
        print(f"{card.name}: {card.cardCode}")
        add_csv_line(card, result_file, [])

    result_file.close()

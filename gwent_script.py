import json
import re
import os
import time
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pathlib import Path
from common import create_template, build_synonyms

version = int(round(time.time() * 1000))
Path("result/gwent/html").mkdir(parents=True, exist_ok=True)
Path("result/gwent/images").mkdir(parents=True, exist_ok=True)


@dataclass_json
@dataclass
class CardData:
    id: str
    name_en: str
    category: str
    faction: str
    power: str
    armor: str
    provision: str
    provisionLeader: str
    color: str
    type: str
    rarity: str
    ability_en_html: str
    artid: str

    def has_armor(self):
        return int(self.armor) > 0

    def has_power(self):
        return int(self.power) > 0

    def has_provisions(self):
        return int(self.provision) > 0

    def has_leader_provisions(self):
        return int(self.provisionLeader) > 0


card_template = create_template("data/gwent/card.html")
glossary_template = create_template("data/gwent/glossary.html")
csv_row_template = create_template("data/csv_row.csv")


def handle(card: CardData, file, synonyms: dict):
    print(f"{card.id} {card.name_en}")
    filename = to_filename(card)
    html_file = f"result/gwent/html/{filename}.html"
    jpg_file = f"result/gwent/images/{filename}.jpg"
    render_card(card, html_file, jpg_file)
    add_csv_line(card, file, filename, get_current_synonyms(card, synonyms))


def get_current_synonyms(card: CardData, synonyms: dict):
    if card.name_en in synonyms.keys():
        return synonyms[card.name_en]
    else:
        return []


def add_csv_line(card, file, filename, current_synonyms: list):
    glossary_html = glossary_template.render(card=card, jpg_file=f"{filename}.jpg", version=version)
    if "'" in card.name_en:
        synonyms = card.name_en.replace("'", "")
        if synonyms not in current_synonyms:
            current_synonyms.append(synonyms)
    description = glossary_html.replace("\"", "\"\"")
    new_synonyms = ",".join(current_synonyms)
    category = "gwent_card"
    glossary = csv_row_template.render(card_name=card.name_en, description=description, synonyms=new_synonyms, category=category)
    file.write(f"{glossary}\n")


def render_card(card, html_file, jpg_file):
    result_html_file = open(html_file, "w", encoding='utf-8')
    result_html_file.write(card_template.render(card=card))
    result_html_file.close()
    os.system(f"wkhtmltoimage --crop-w 249 --crop-h 357 --crop-x 8 --crop-y 8  --quality 100 {html_file} {jpg_file}")


def to_filename(card: CardData):
    filename = card.name_en.lower().replace(" ", "_")
    filename = re.sub(r'\W+', '', filename)
    return filename


if __name__ == '__main__':
    synonyms_dict = build_synonyms("gwent_card")

    result_file = open('result/gwent/gwent-import.csv', 'w', encoding='utf-8')
    result_file.write('"Id","Title","Excerpt","Description","Synonyms","Variations","Categories"\n')
    with open('data/gwent/cards.json', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    d = json.loads(data)
    n = 906
    for i in range(0, n):
        print(f"{i}/{n}")
        card = CardData.from_dict(d[str(i)])
        handle(card, result_file, synonyms_dict)

    result_file.close()

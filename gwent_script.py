import json
import math
import re
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pathlib import Path
from common import create_template, build_synonyms

version = int(round(time.time() * 1000))
Path("result/gwent/html").mkdir(parents=True, exist_ok=True)
Path("result/gwent/images").mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=8)

@dataclass_json
@dataclass
class CardData:
    id: str
    name: str
    category: str
    faction: str
    power: str
    armor: str
    provision: str
    color: str
    type: str
    rarity: str
    abilityHTML: str
    artid: str

    def has_armor(self):
        return int(self.armor) > 0

    def has_power(self):
        return int(self.power) > 0

    def has_provisions(self):
        return (not self.has_leader_provisions()) and int(self.provision) > 0

    def has_leader_provisions(self):
        return self.category == "Leader"

    def get_type(self):
        if self.category.lower() == "leader":
            return "leader"
        if self.type.lower() == "special":
            return "spell"
        else:
            return self.type.lower()


card_template = create_template("data/gwent/card.html")
glossary_template = create_template("data/gwent/glossary.html")
csv_row_template = create_template("data/csv_row.csv")


def handle(card: CardData, file, synonyms: dict):
    print(f"{card.id} {card.name}")
    filename = to_filename(card)
    html_file = f"result/gwent/html/{filename}.html"
    jpg_file = f"result/gwent/images/{filename}.jpg"
    executor.submit(render_card, card, html_file, jpg_file)
    # render_card(card, html_file, jpg_file)
    add_csv_line(card, file, filename, get_current_synonyms(card, synonyms))


def get_current_synonyms(card: CardData, synonyms: dict):
    if card.name in synonyms.keys():
        return synonyms[card.name]
    else:
        return []


def add_csv_line(card, file, filename, current_synonyms: list):
    glossary_html = glossary_template.render(card=card, jpg_file=f"{filename}.jpg", version=version)
    if "'" in card.name:
        synonyms = card.name.replace("'", "")
        if synonyms not in current_synonyms:
            current_synonyms.append(synonyms)
    description = glossary_html.replace("\"", "\"\"")
    new_synonyms = ",".join(current_synonyms)
    category = "gwent_card"
    glossary = csv_row_template.render(card_name=card.name, description=description, synonyms=new_synonyms, category=category)
    file.write(f"{glossary}\n")


def render_card(card, html_file, jpg_file):
    result_html_file = open(html_file, "w", encoding='utf-8')
    result_html_file.write(card_template.render(card=card))
    result_html_file.close()
    os.system(f"wkhtmltoimage --crop-w 249 --crop-h 357 --crop-x 8 --crop-y 8  --quality 100 {html_file} {jpg_file}")


def to_filename(card: CardData):
    filename = card.name.lower().replace(" ", "_")
    filename = re.sub(r'\W+', '', filename)
    return filename


if __name__ == '__main__':
    synonyms_dict = build_synonyms("gwent_card")

    with open('data/gwent/cards.json', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    d = json.loads(data)
    n = len(d.keys())
    max_per_file = 500
    files_num = math.ceil(n/500)
    print(f"n={n}")
    print(f"files_num={files_num}")

    for f in range(0, files_num):
        print(f"File {f+1}/{files_num}")
        result_file = open(f'result/gwent/gwent-import_{f}.csv', 'w', encoding='utf-8')
        result_file.write('"Id","Title","Excerpt","Description","Synonyms","Variations","Categories"\n')
        start = f * max_per_file
        for i in range(start, start + max_per_file):
            if i < n:
                print(f"Card {i+1}/{n}")
                card = CardData.from_dict(d[str(i)])
                handle(card, result_file, synonyms_dict)
        result_file.close()

    executor.shutdown()

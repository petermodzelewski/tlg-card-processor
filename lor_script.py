import json
import time
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json
from pathlib import Path
from common import create_template, build_synonyms

version = int(round(time.time() * 1000))
Path("result/lor").mkdir(parents=True, exist_ok=True)


@dataclass_json
@dataclass
class CardData:
    name: str
    cardCode: str
    associatedCardRefs: List[str]
    collectible: bool
    supertype: str

    def get_card_codes(self):
        result = [self.cardCode]
        result.extend(self.associatedCardRefs)
        return result

    def should_process(self):
        return (self.supertype is not "Champion") or self.collectible


def get_current_synonyms(card: CardData, synonyms: dict):
    if card.name in synonyms.keys():
        return synonyms[card.name]
    else:
        return []


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
    glossary = csv_row_template.render(card_name=card.name, description=description, synonyms=new_synonyms,
                                       category=category)
    file.write(f"{glossary}\n")


if __name__ == '__main__':
    synonyms_dict = build_synonyms("lor_card")

    result_file = open('result/lor/lor-import.csv', 'w', encoding='utf-8')
    result_file.write('"Id","Title","Excerpt","Description","Synonyms","Variations","Categories"\n')

    with open('data/lor/cards.json', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')

    d = json.loads(data)
    for card_data in d:
        card = CardData.from_dict(card_data)
        print(f"{card.name}: {card.cardCode}")
        if card.should_process():
            add_csv_line(card, result_file, get_current_synonyms(card, synonyms_dict))

    result_file.close()

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


def get_current_synonyms(card_name: str, synonyms: dict):
    if card_name in synonyms.keys():
        return synonyms[card_name]
    else:
        return []


glossary_template = create_template("data/lor/lor_card_glossary.html")
csv_row_template = create_template("data/csv_row.csv")


def add_csv_line(card_name: str, cards: list, file, current_synonyms: list):
    codes = [x.cardCode for x in cards]
    glossary_html = glossary_template.render(version=version, codes=codes)
    description = glossary_html.replace("\"", "\"\"")
    if "'" in card_name:
        synonyms = card_name.replace("'", "")
        if synonyms not in current_synonyms:
            current_synonyms.append(synonyms)
    new_synonyms = ",".join(current_synonyms)
    category = "lor_card"
    glossary = csv_row_template.render(card_name=card_name, description=description, synonyms=new_synonyms,
                                       category=category)
    file.write(f"{glossary}\n")


def process_cards_file(cards_file: str):
    with open(f"data/lor/{cards_file}", 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')
    d = json.loads(data)
    cards = [CardData.from_dict(card_data) for card_data in d]
    cards_by_code = {}
    for card in cards:
        cards_by_code[card.cardCode] = card
    for card in cards:
        if (card.supertype == "Champion") and card.collectible:
            associated_cards = [cards_by_code[code] for code in card.associatedCardRefs]
            lvl2_card = [card for card in associated_cards if card.supertype == "Champion"][0]
            print(f"Adding champion {card.name}, {lvl2_card.name}")
            add_csv_line(card.name, [card, lvl2_card], result_file, get_current_synonyms(card.name, synonyms_dict))
        else:
            if card.supertype != "Champion":
                print(f"Adding regular {card.name}")
                add_csv_line(card.name, [card], result_file, get_current_synonyms(card.name, synonyms_dict))
            # else:
            #     print(f"Ignoring {card}")


if __name__ == '__main__':
    synonyms_dict = build_synonyms("lor_card")

    for file in ["set1-en_us.json", "set2-en_us.json", "set3-en_us.json", "set4-en_us.json"]:
        set = file.split("-")[0]
        result_file = open(f"result/lor/lor-import-{set}-.csv", 'w', encoding='utf-8')
        result_file.write('"Id","Title","Excerpt","Description","Synonyms","Variations","Categories"\n')
        process_cards_file(file)
        result_file.close()

# TLG card processor

## Setup
1) Get https://wkhtmltopdf.org and have `wkhtmltoimage` in your system `PATH` env 
2) Install python, conda etc 
3) Install dependencies (preferably after creating python env for this project)
```
pip install -r requirements.txt
```

## Gwent

### Preparation
* Make sure that `data/gwent/cards.json` is the newest one from https://gwent.one/api/cardlist
```
curl https://gwent.one/api/cardlist --output data/gwent/cards.json
```
* Make sure that `data/export.csv` is the newest export from glossary plugin from wordpress

### Generating data 
* Run `gwent_script.py`. It takes a while.

### Upload
* Copy files from `result/gwent/images` to `/public_html/wp-content/uploads/gwent_cards` on 184.168.146.20
* Upload `result/gwent/gwent-import.csv` in the glossary plugin settings in wordpress

## LOR
### Preparation
* Make sure that `data/lor/cards.json` is the newest one from https://developer.riotgames.com/docs/lor#data-dragon_core-bundles  (https://dd.b.pvp.net/latest/core-en_us.zip pack)
* Make sure that `data/export.csv` is the newest export from glossary plugin from wordpress

### Generating data 
* Run `lor_script.py`

### Upload
* Copy files from the pack to `/public_html/wp-content/uploads/lor_cards` on 184.168.146.20
* Upload `result/lor/lor-import.csv` in the glossary plugin settings in wordpress
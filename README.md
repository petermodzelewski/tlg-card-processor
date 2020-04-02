# tlg-card-processor

## Setup
1) Get https://wkhtmltopdf.org and have `wkhtmltoimage` in your system `PATH` env 
2) Install python, conda etc 
3) Install dependencies (preferably after creating python env for this project)
```
pip install -r requirements.txt
```

## Prepare

1) Make sure that `cards.json` is the newest one from https://gwent.one/api/cardlist
```
curl https://gwent.one/api/cardlist --output cards.json
```
2) Make sure that `export.csv` is the newest export from glossary plugin from wordpress

## Run script

Run `script.py`. It takes a while.

## Upload data

1) Copy files from `./images` to `/public_html/wp-content/uploads/gwent_cards` on 184.168.146.20
2) Upload `import.csv` in the glossary plugin settings in wordpress
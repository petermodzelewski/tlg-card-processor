#!/bin/bash
rm -rf result/lor/cards
mkdir -p result/lor/cards

declare -a SetArray=("1" "2" "3" "4")

for val in ${SetArray[@]}; do
  SET="set$val-en_us"
  FILE="$SET.zip"
  rm -rf result/lor/$FILE
  curl https://dd.b.pvp.net/latest/$FILE --output result/lor/$FILE
  unzip result/lor/$FILE -d result/lor/$SET
  mv result/lor/$SET/en_us/img/cards/*.png result/lor/cards/
  mv result/lor/$SET/en_us/data/*.json data/lor/
done



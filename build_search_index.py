import urllib2
import os.path
import json
from pprint import pprint
from fuzzywuzzy import process
import os

VERSION_FILE = 'data/version.txt'
DATA_FILE = 'data/all-sets.json'
TEMP_FILE = 'tmp'
INPUT_DIRECTORY = 'input'

# check to see if stored version of card data is outdated
new_version = urllib2.urlopen('http://mtgjson.com/json/version.json').read()

old_version = ""
if os.path.isfile(VERSION_FILE):
    with open(VERSION_FILE, 'r') as f:
        old_version = f.read()

if new_version != old_version:
    with open(VERSION_FILE, 'w') as f:
        f.write(new_version)

    new_data = urllib2.urlopen('http://mtgjson.com/json/AllSets-x.json')
    print "Fetching version " + new_version + " of the json data.  Please wait."
    with open(DATA_FILE, 'w') as f:
        f.write(new_data.read())

all_cards = ""
with open(DATA_FILE, 'r') as f:
    json_data = f.read()
    all_cards = json.loads(json_data)

# pprint(all_cards["LEA"]["cards"][0])

all_unique_card_names = set()

for card_set in all_cards.values():
    for card in card_set["cards"]:
        all_unique_card_names.add(card["name"])

pprint(process.extract('Shittestrm', list(all_unique_card_names), limit=3))
pprint(process.extract('Viashinoa Skanktile', list(all_unique_card_names), limit=3))

#set the language location
os.environ['TESSDATA_PREFIX'] = '/home/brian/dev/tesseract-ocr-3.02'

#attempt to identify each card
for card in os.listdir(INPUT_DIRECTORY):
    os.system('tesseract ' + INPUT_DIRECTORY + '/' + card  + TEMP_FILE)

    with open(TEMP_FILE + '.txt', 'r') as f:
        found_text = f.read().strip()
        print found_text

    pprint(process.extract(found_text, list(all_unique_card_names), limit=3))

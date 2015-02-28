import urllib2
import os.path
import json
from pprint import pprint
from fuzzywuzzy import process
import os
import cv2

VERSION_FILE = 'data/version.txt'
DATA_FILE = 'data/all-sets.json'
TEMP_FILE = 'tmp'
TEMP_FULL_TEXT_FILE = 'tmp-full-text'
INPUT_DIRECTORY = 'input'
CROPPED_DIRECTORY = 'cropped'


def check_output(tmp_file):
    success = True
    with open(tmp_file, 'r') as f:
        found_text = f.read().strip()
        print "Found text:" + found_text
        if len(found_text) == 0:  # error condition
            success = False

        return (success, found_text)

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

# set the language location
os.environ['TESSDATA_PREFIX'] = '/home/brian/dev/tesseract-ocr-3.02'

failed_to_identify = []

# attempt to identify each card
for card in os.listdir(INPUT_DIRECTORY):
    if card == '.gitignore':
        continue

    card_path = INPUT_DIRECTORY + '/' + card
    print card_path
    image = cv2.imread(card_path)
    crop_image = image[100:150, 50:1300]
    cropped_path = CROPPED_DIRECTORY + '/' + card
    cv2.imwrite(cropped_path, crop_image)

    os.system('tesseract ' + cropped_path + ' ' + TEMP_FILE)

    tmp_file = TEMP_FILE + '.txt'
    result = check_output(tmp_file)
    full_text = ''

    if not result[0]:  # error condition, retry
        os.system('tesseract -psm 7 ' + cropped_path + ' ' + TEMP_FILE)
        result = check_output(tmp_file)

    #os.system('tesseract ' + card_path + ' ' + TEMP_FULL_TEXT_FILE)
    #full_text = check_output(TEMP_FULL_TEXT_FILE + '.txt')

    possible = process.extract(result[1], list(all_unique_card_names), limit=3)
    if possible[0][1] < 70:
        failed_to_identify.append([cropped_path, result[1]])
    else:
        pprint(possible[0])
        #pprint(full_text)

print "Failures:"
pprint(failed_to_identify)

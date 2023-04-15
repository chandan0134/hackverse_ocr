import pytesseract
import pdf2image
import spacy
import regex as re
import json


images = pdf2image.convert_from_path("sample2.pdf",500,poppler_path=r'C:\Program Files\Release-23.01.0-0\poppler-23.01.0\Library\bin')

text = ''
for img in images:
    text += pytesseract.image_to_string(img)


nlp = spacy.load('en_core_web_sm')
doc = nlp(text)


name_match = re.search('name\s*:\s*(.+)', text, re.IGNORECASE)
name = name_match.group(1) if name_match else ''

wallet_address_match = re.search('(?i)wallet address\s*:\s*(\w+)', text,re.IGNORECASE)
wallet_address = wallet_address_match.group(1) if wallet_address_match else ''



occupation_name_match = re.search('occupation\s*:\s*(.+)', text, re.IGNORECASE)
occupation_name = occupation_name_match.group(1).strip() if occupation_name_match else ''


product_name_match = re.search('product name\s*:\s*(.+)', text, re.IGNORECASE)
product_name = product_name_match.group(1).strip() if product_name_match else ''



product_price_match = re.search('product price\s*:\s*\$?([\d,]+(?:\.\d{1,2})?)', text, re.IGNORECASE)
product_price = product_price_match.group(1).replace(',', '') if product_price_match else '0.00'



    
data = {'name': name, 'wallet address': wallet_address, 'product name': product_name, 'product price': product_price,'occupation':occupation_name}
with open('output.json', 'w') as f:
    json.dump(data, f)









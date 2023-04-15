# import pytesseract
# import pdf2image
# import spacy
# import regex as re
# import json


# images = pdf2image.convert_from_path("sample.pdf",500,poppler_path=r'C:\Program Files\Release-23.01.0-0\poppler-23.01.0\Library\bin')

# text = ''
# for img in images:
#     text += pytesseract.image_to_string(img)


# nlp = spacy.load('en_core_web_sm')
# doc = nlp(text)
# name = ''

# wallet_address = ''
# for ent in doc.ents:
#     if ent.label_ == 'PERSON':
#         name = ent.text
#     elif ent.label_ == 'ADDRESS':
#         wallet_address = ent.text
        


# product_name_match = re.search('product name\s*:\s*(.+)', text, re.IGNORECASE)
# product_name = product_name_match.group(1).strip() if product_name_match else ''



# product_price_match = re.search('product price\s*:\s*\$?([\d,]+(?:\.\d{1,2})?)', text, re.IGNORECASE)
# product_price = product_price_match.group(1).replace(',', '') if product_price_match else '0.00'



    
# data = {'name': name, 'wallet address': wallet_address, 'product name': product_name, 'product price': product_price}
# with open('output.json', 'w') as f:
#     json.dump(data, f)








import pytesseract
import pdf2image
import spacy
import regex as re
import json

images = pdf2image.convert_from_path("sample.pdf", 500, poppler_path=r'C:\Program Files\Release-23.01.0-0\poppler-23.01.0\Library\bin')
text = ''
for img in images:
    text += pytesseract.image_to_string(img)

# Extract name and wallet address using spaCy's Named Entity Recognition (NER)
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
name = ''
wallet_address = ''
for ent in doc.ents:
    if ent.label_ == 'PERSON':
        name = ent.text
    elif ent.label_ == 'ADDRESS':
        wallet_address = ent.text

product_name_match = re.search('product name\s*:\s*(.+)', text, re.IGNORECASE)
product_name = product_name_match.group(1).strip() if product_name_match else ''

product_price_match = re.search('product price\s*:\s*\$?([\d,]+(?:\.\d{1,2})?)', text, re.IGNORECASE)
product_price = product_price_match.group(1).replace(',', '') if product_price_match else '0.00'

# Store extracted information in a JSON file
data = {'product name': product_name, 'product price': product_price}
if name:
    data['name'] = name
if wallet_address:
    data['wallet address'] = wallet_address

with open('output.json', 'w') as f:
    json.dump(data, f)

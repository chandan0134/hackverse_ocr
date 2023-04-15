from flask import Flask, request, jsonify
import pytesseract
import pdf2image
import spacy
import regex as re

app = Flask(__name__)


@app.route('/extract', methods=['POST'])
def extract_information():
    # Get the PDF file from the request
    pdf_file = request.files['pdf_file']

    # Convert the PDF file to images
    images = pdf2image.convert_from_bytes(pdf_file.read(), 200)

    # Use OCR to extract text from the images
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)

    # Use spaCy to analyze the text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # Use regular expressions to extract the relevant information
    name_match = re.search('name\s*:\s*(.+)', text, re.IGNORECASE)
    name = name_match.group(1) if name_match else ''

    wallet_address_match = re.search('(?i)wallet address\s*:\s*(\w+)', text, re.IGNORECASE)
    wallet_address = wallet_address_match.group(1) if wallet_address_match else ''

    occupation_name_match = re.search('occupation\s*:\s*(.+)', text, re.IGNORECASE)
    occupation_name = occupation_name_match.group(1).strip() if occupation_name_match else ''

    product_name_match = re.search('product name\s*:\s*(.+)', text, re.IGNORECASE)
    product_name = product_name_match.group(1).strip() if product_name_match else ''

    product_price_match = re.search('product price\s*:\s*\$?([\d,]+(?:\.\d{1,2})?)', text, re.IGNORECASE)
    product_price = product_price_match.group(1).replace(',', '') if product_price_match else '0.00'

    # Create a dictionary containing the extracted information
    data = {'name': name, 'wallet address': wallet_address, 'product name': product_name,
            'product price': product_price, 'occupation': occupation_name}

    # Convert the dictionary to JSON format and return it in the response
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)

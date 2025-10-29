import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ocr_utils import extract_text_from_file
from translate_utils import translate_text
from storage import save_document_record
from dotenv import load_dotenv


load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
# Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}

# Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

# Translate endpoint
@app.route('/translate', methods=['POST'])
def translate():
    # Check file
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Get source and target languages
    src_lang = request.form.get('src_lang', 'pt')
    target_langs = request.form.get('target_langs', 'en,hi').split(',')

    # Extract text from file (PDF/images)
    # This now correctly returns a single string from ocr_utils.py
    extracted_text = extract_text_from_file(filepath, src_lang=src_lang)

    # === FIX STARTS HERE ===
    # Create a dictionary to hold the translations
    translations = {}
    # Loop through each target language and translate the text
    for lang in target_langs:
        # Call the translation function for each language individually
        translated_text = translate_text(extracted_text, src_lang=src_lang, tgt_lang=lang)
        translations[lang] = translated_text
    # === FIX ENDS HERE ===

    # Save record to database (MongoDB)
    record = {
        "filename": filename,
        "src_lang": src_lang,
        "target_langs": target_langs,
        "extracted_text": extracted_text,
        "translations": translations  # Save the dictionary of translations
    }
    doc_id = save_document_record(record)

    # Return JSON response
    return jsonify({
        "id": str(doc_id),
        "extracted_text": extracted_text,
        "translations": translations
    })

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
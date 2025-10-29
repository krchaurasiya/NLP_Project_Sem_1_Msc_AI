from transformers import pipeline

# ✅ Use a reliable multilingual translation model from Facebook
# This model can translate between 100+ languages (including Portuguese ↔ English)
translator = pipeline("translation", model="facebook/m2m100_418M")

def translate_text(text, src_lang='pt', tgt_lang='en'):
    """
    Translate text from source language to target language using M2M100 model.
    """
    if not text.strip():
        return ""

    try:
        result = translator(text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=1000)
        return result[0]['translation_text']
    except Exception as e:
        print("Translation error:", e)
        return f"Error: {str(e)}"

# import json

# # Load Hindi-Konkani dictionary
# with open("data/hindi_konkani_dict.json", "r", encoding="utf-8") as f:
#     hindi_konkani_dict = json.load(f)




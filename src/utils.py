import pdfplumber
import requests
import os
import uuid

from src.tokenize.tokenize_text import preprocess_text


def pdf_text_extraction(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            all_text += text
        return all_text


def download_text_cv_from_url(url):
    response = requests.get(url)

    unique_id = uuid.uuid4()

    if response.status_code == 200:
        filename = f"cv_{unique_id}.pdf"
        with open(filename, "wb") as file:
            file.write(response.content)

        text = pdf_text_extraction(filename)
        os.remove(filename)
    else:
        text = ""

    return text


def get_skills_from_cv(model, vectorizer, url):
    cv_text = download_text_cv_from_url(url)

    cv_tokens = preprocess_text(cv_text)

    cv_tfidf = vectorizer.transform(cv_tokens)

    cv_predictions = model.predict(cv_tfidf)

    skills = [cv_tokens[i]
              for i in range(len(cv_predictions)) if cv_predictions[i] == 1]

    return ' '.join(skills)

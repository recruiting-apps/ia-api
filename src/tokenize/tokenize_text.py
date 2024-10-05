import string
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

excluded_words = {'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
                  'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'}


def clean_and_segment_text(text):
    text = re.sub(r'\s+', ' ', text.replace('\n', ' '))

    # Eliminar correos electrónicos
    text = re.sub(r'\S+@\S+', '', text)

    # Eliminar números de teléfono
    text = re.sub(r'\+?\d[\d -]{8,12}\d', '', text)

    # Eliminar fechas
    text = re.sub(r'\d{2}-\d{2}-\d{4}', '', text)

    text = text.replace('-', '')

    # Convertir a minúsculas y eliminar puntuación
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text


def preprocess_text(text):
    text = clean_and_segment_text(text)
    tokens = nltk.word_tokenize(text)

    tokens = [word for word in tokens if len(
        word) > 3 and word not in excluded_words]

    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words]

    # tokens = [token.lemma_ for token in nlp(
    #     ' '.join(tokens)) if not token.is_stop]

    return tokens

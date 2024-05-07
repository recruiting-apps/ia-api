import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize, sent_tokenize

nltk.download('punkt')


def tokenize(skills):
    # skills = [skills]
    # skills = ''.join(skills)
    # print('skills', skills)

    tokens = word_tokenize(skills)

    # Eliminar puntuación y números
    tokens = [word for word in tokens if word.isalpha()]

    # Unir tokens preprocesados en una cadena de texto nuevamente
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text


def generate_tfidf_matrix(preprocessed_text):
    # Representación de texto mediante TF-IDF
    corpus = [preprocessed_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Obtener vocabulario (opcional, para conocer las características)
    vocab = vectorizer.get_feature_names_out()

    # Mostrar el resultado del TF-IDF para cada término
    for i, word in enumerate(vocab):
        print(f"Palabra: {word}, TF-IDF: {tfidf_matrix[0, i]}")  # type: ignore

    return tfidf_matrix

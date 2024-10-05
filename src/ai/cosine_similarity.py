from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# job_offer: texto preprocesado de la oferta de trabajo
# cvs: lista de cvs (skills extraidos)


def generate_vectors(job_offer, cvs):
    documents = cvs + [job_offer]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    job_offer_vector = tfidf_matrix[-1]
    cv_vectors = tfidf_matrix[:-1]

    return [job_offer_vector, cv_vectors]


def calculate_similarity(vector1, vector2):
    similarities = cosine_similarity(vector1, vector2)[0]

    return similarities

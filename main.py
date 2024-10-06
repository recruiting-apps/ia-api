from flask import Flask, request
from flask_cors import CORS

from src.ai.cosine_similarity import calculate_similarity, generate_vectors
from src.ai.svm_model import get_svm_model, preprocess_text
from src.utils import get_skills_from_cv

from config import PORT

app = Flask(__name__)
CORS(app)

model, vectorizer = get_svm_model()


def sort_applications(applications, similarities):
    sorted_applications = sorted(
        zip(applications, similarities), key=lambda x: x[1], reverse=True)

    return [application[0] for application in sorted_applications]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/find-better-applicant', methods=['POST'])
def find_better_applicant():
    request_data = request.get_json()

    offer = request_data['offer']
    applications = request_data['applications']

    cvs = [application['user']['cvPath']
           for application in applications]

    cv_skills = [get_skills_from_cv(
        model, vectorizer, cv_path) for cv_path in cvs]

    job_offer_tokens = ' '.join(preprocess_text(offer))
    job_offer_tfidf, cvs_tfidf = generate_vectors(job_offer_tokens, cv_skills)

    similarities = calculate_similarity(job_offer_tfidf, cvs_tfidf)

    sorted_applications = sorted(
        zip(applications, similarities), key=lambda x: x[1], reverse=True)

    return [application_order[0] for application_order in sorted_applications]


if __name__ == '__main__':
    app.run(debug=True, port=PORT)

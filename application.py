from flask import Flask, request
from flask_cors import CORS
from config import PORT

from src.utils import download_file, remove_file, sort_applications
from src.pdf.read_pdf import get_content
from src.tokenize.tokenize_pdf import tokenize, generate_tfidf_matrix
from src.ai.svm_predict_skills import train_model_with_csv
from src.ai.calculate_similarity import calculate_similarity

application = Flask(__name__)
prediction_model = train_model_with_csv('')
CORS(application)


@application.route('/')
def helloWorld():
    return 'Hello World!'


@application.route('/find-better-applicant', methods=['POST'])
def index():
    request_data = request.get_json()
    print(request_data)
    offer = request_data['offer']
    applications = request_data['applications']

    cvs = [(application['user']['cvPath'], application['user']['id'])
           for application in applications]

    cvs_content = []

    root_path = application.root_path

    for cv_path, cv_id in cvs:
        os_path = f'{root_path}\\src\\pdf-download\\{cv_id}.pdf'
        download_file(cv_path, os_path)
        try:
            cv_content = get_content(os_path)
            cvs_content.append((cv_id, cv_content))
            remove_file(os_path)
        except:
            pass

    cvs_labels = []
    for cv_id, cv_content in cvs_content:
        if prediction_model:
            cvs_labels.append((cv_id, cv_content, tokenize(
                prediction_model.predict([cv_content])[0])))  # type: ignore

    expected_skills = tokenize(', '.join(offer['expectedAbilities']))
    tfidf_expected_matrix = generate_tfidf_matrix(expected_skills)

    similarities, indexes = calculate_similarity(tfidf_expected_matrix, [
        generate_tfidf_matrix(cv_label[2]) for cv_label in cvs_labels])

    # Get applicants order by similarity desc
    # Order the applications by indexes order
    applications = sort_applications(applications, similarities, indexes)
    return applications


if __name__ == '__main__':
    application.run(debug=True, port=PORT)

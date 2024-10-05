import spacy

from src.ai.cosine_similarity import calculate_similarity, generate_vectors
from src.ai.svm_model import get_svm_model
from src.tokenize.tokenize_text import preprocess_text
from src.utils import download_text_cv_from_url, get_skills_from_cv

nlp = spacy.load('en_core_web_sm')


def test_model_prediction():
    model, vectorizer = get_svm_model()
    cvs = [{
        "id": 1,
        "url": "https://firebasestorage.googleapis.com/v0/b/recruitingapp-8355f.appspot.com/o/RENATO%20ARREDONDO%20CV.pdf?alt=media&token=f8519829-28f4-4ee7-96f2-ed25330e3ba8"
    },
        {
            "id": 2,
            "url": "https://firebasestorage.googleapis.com/v0/b/recruitingapp-8355f.appspot.com/o/RENATO%20ARREDONDO%20CV.pdf?alt=media&token=f8519829-28f4-4ee7-96f2-ed25330e3ba8"
    },
        {
            "id": 1,
            "url": "https://firebasestorage.googleapis.com/v0/b/recruitingapp-8355f.appspot.com/o/RENATO%20ARREDONDO%20CV.pdf?alt=media&token=f8519829-28f4-4ee7-96f2-ed25330e3ba8"
    },
        {
            "id": 2,
            "url": "https://firebasestorage.googleapis.com/v0/b/recruitingapp-8355f.appspot.com/o/RENATO%20ARREDONDO%20CV.pdf?alt=media&token=f8519829-28f4-4ee7-96f2-ed25330e3ba8"
    }]

    cv_skills = [get_skills_from_cv(
        model, vectorizer, cv["url"]) for cv in cvs]

    job_offer = """
        Estamos en búsqueda de un Desarrollador Web con experiencia en React para unirse a nuestro equipo de tecnología. 
        El candidato ideal será responsable de crear y mantener aplicaciones web de alto rendimiento, trabajando de cerca con 
        diseñadores y desarrolladores backend para entregar soluciones escalables y eficientes.

        Requisitos:
        - Experiencia demostrable de al menos 2 años en desarrollo web utilizando React.
        - Conocimientos sólidos en TypeScript, HTML, CSS, y TailwindCSS.
        - Experiencia con herramientas de construcción como Webpack, Babel y npm.
        - Conocimientos en el manejo de sistemas de control de versiones como Git.
        - Familiaridad con el manejo del estado de la aplicación usando Redux o Context API.
        - Experiencia en el desarrollo responsive y cross-browser.
        - Conocimientos en lenguajes backend como Python y Java.
    """

    job_offer_tokens = ' '.join(preprocess_text(job_offer))
    job_offer_tfidf, cv1_tfidf = generate_vectors(job_offer_tokens, cv_skills)

    similarities = calculate_similarity(job_offer_tfidf, cv1_tfidf)

    results = [{"cv_id": cvs[i]["id"], "similarity": similarities[i]}
               for i in range(len(similarities))]

    print(results)


if __name__ == "__main__":
    print("main")
    test_model_prediction()

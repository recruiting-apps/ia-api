import pandas as pd
import joblib
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import string
import os

nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')


def preprocess_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))

    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words]

    lemmatized_tokens = [token.lemma_ for token in nlp(' '.join(tokens))]

    return ' '.join(lemmatized_tokens)


def calculate_better_configuration(model, X_train, y_train):

    # Definir los hiperparámetros a probar en Grid Search
    param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [
        1, 0.1, 0.01, 0.001], 'kernel': ['linear', 'rbf']}

    grid_search = GridSearchCV(
        model, param_grid, cv=5, scoring='accuracy', verbose=2)

    grid_search.fit(X_train, y_train)

    print("Precisión del modelo en validación cruzada:",
          grid_search.best_score_)
    return grid_search.best_params_


def train_svm():
    file_path = os.path.join(os.path.dirname(
        __file__), "src/ai/skills_dataset.csv")
    data = pd.read_csv(file_path)

    X = data["text"].apply(preprocess_text)
    y = data["is_skill"]

    # Vectorización con TF-IDF
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42)

    model = svm.SVC(C=10, gamma=0.1, kernel='rbf')

    # Encontrar la mejor configuración de hiperparámetros
    # best_params = calculate_better_configuration(model, X_train, y_train)
    # print("Mejores hiperparámetros encontrados:", best_params)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Precisión del modelo:", f"{accuracy*100:.4f}%")

    joblib.dump(model, "svm_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    return model, vectorizer


def get_svm_model():
    model = None
    vectorizer = None
    try:
        model = joblib.load("svm_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
    except:
        model, vectorizer = train_svm()
        joblib.dump(model, "svm_model.pkl")
        joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

    return model, vectorizer


if __name__ == "__main__":
    train_svm()

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# X (contenido del cv)
# y (etiquetas de habilidades)

def train_prediction_skills(X, y):
  # Dividir los datos en conjuntos de entrenamiento y prueba
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Inicializar y entrenar un clasificador SVM
  clf = SVC(kernel='linear', C=1.0, random_state=42)
  clf.fit(X_train, y_train)

  # Predecir las habilidades para los CVs de prueba
  predicciones = clf.predict(X_test)

  # Evaluar la precisión del modelo
  precision = accuracy_score(y_test, predicciones)
  print(f"Precisión del modelo: {precision}")

  # Obtener un informe detallado de la clasificación
  print(classification_report(y_test, predicciones))

  return clf

def predict_skills(model, X):
  # Predecir las habilidades para los CVs de prueba
  predicciones = model.predict(X)

  return predicciones

def train_model_with_csv(csv_path):
  if csv_path == '':
    return None

  # Leer el CSV
  df = pd.read_csv(csv_path)

  # Obtener las columnas de habilidades
  skills = df.columns[1:]

  # Obtener las habilidades requeridas
  y = df[skills]

  # Obtener el contenido de los CVs
  X = df['content']

  # Entrenar el modelo
  model = train_prediction_skills(X, y)

  return model
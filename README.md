# Configuración del Entorno y Levantamiento del Servidor Flask

Este README proporciona instrucciones para configurar un entorno de desarrollo con Python, instalar las dependencias necesarias, crear un archivo .env con un puerto personalizado y levantar un servidor Flask utilizando el archivo app.py.

## Pasos a seguir

1. Clona el repositorio en tu máquina local:

  ```bash
  git clone https://github.com/recruiting-apps/ia-api.git
  ```

2. Navega al directorio del proyecto:

  ```bash
  cd tu-repositorio
  ```

3. Crea un entorno virtual para el proyecto:

  ```bash
  python -m venv env
  ```

4. Activa el entorno virtual:

  - En Windows:

    ```bash
    env\Scripts\activate
    ```

  - En macOS y Linux:

    ```bash
    source env/bin/activate
    ```

5. Instala las dependencias del proyecto:

  ```bash
  pip install -r requirements.txt
  ```

6. Crea un archivo `.env` en el directorio del proyecto y define el puerto personalizado:

  ```plaintext
  PORT=8080
  ```

7. Ejecuta el servidor Flask:

  ```bash
  python application.py
  ```

8. Abre tu navegador web y visita `http://localhost:8080` para ver la aplicación en funcionamiento.

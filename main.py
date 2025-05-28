"""
Imagina que esta API es una biblioteca de peliculas:
La funcion load_movies() es como un bibliotecario que carga el cataogo de
libros (peliculas) cuando se abre la biblioteca.
La funcion get_movies() muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie() es como si alguien preguntara por uin libro especifico
por su codigo de identificacion.
La funcion chatbot (query) es un asistente que busca libros segun palabras clave
y sinonimo.
La funcion get_movie_by_category (category) ayuda a encontrar peliculas segun su
genero (accion, comedia, etc).
"""

# Importamos las herramientas necesarias para construir nuestra API
from fastapi import FastAPI, HTTPException  # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse  # HTMLResponse para paginas web, JSONResponse para respuestas en formato JSON
import pandas as pd  # Pandas es una herramienta para manejar datos en tablas.
import nltk  # NLTK es una herramienta para procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize  # Se usa para dividir un texto en palabras individuales.
from nltk.corpus import wordnet  # Nos ayuda a encontrar sinónimos de palabras.
nltk.download('punkt_tab')

# Indicamos la ruta donde NLTK buscará los datos descargados en nuestro computador. Se puede ver ejecutando nltk.download("punkt")
# nltk.data.path.append("/opt/homebrew/lib/python3.9/site-packages/nltk_data")
nltk.data.path.append("/Users/eduardoarbelaez/nltk_data")

# Descargar las herramientas necesarias de NLTK para el analisis de palabras.abs

nltk.download("punkt")  # Herramienta para dividir frases en palabras.
nltk.download("wordnet")  # Herramienta para encontrar sinónimos de palabras en ingles.

# Funcion para cargar ls peliculas desde un archivo CSV.


def load_movies():
    # Leemos el archivo que contiene la informacion de las peliculas y seleccionamos las columnas importantes
    df = pd.read_csv("Dataset/netflix_titles.csv")[['show_id', 'title', 'release_year', 'listed_in', 'rating', 'description']]

    # Renombramos las columnas para que sean mas faciles de entender
    df.columns = ['id', 'title', 'year', 'category', 'rating', 'overview']

    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')


# Cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
movies_list = load_movies()

# Funcion para encontrar sinonimos de una palabra.


def get_synonyms(word):
    # Usamos wordnet para encontrar distintas palabras que significan lo mismo.
    return {lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, qe sera el motor de nuestra API.
# Esto inicializa la API con un nombre y una version.
app = FastAPI(title='Mi app de peliculas', version='1.0.0')


@app.get('/', tags=['Home'])
def home():
    # Cuando entremos en el navegador a http://lo127.0.0.1:8000/ nos mostrara un mensaje de bienvenida.
    return HTMLResponse('<h1> Bienvenido a la API de peliculas </h1>')

# CON ESTE COMANDO EJECUTO LA APP:
# uvicorn main:app --reload --port 5000

# Y ASI ENTRO EN LA DOCUMENTACION DE LA API SWAGGER:
# http://127.0.0.1:5000/docs


# Obteniendo la lista de películas
# Creamos una ruta para obtener todas las películas
# Ruta para obtener todas las películas
@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay películas, las enviamos, si no mostramos un error
    return movies_list or HTMLResponse(status_code=500, detail="No hay datos de películas disponibles")


# ruta para obtener una película específica por su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movies(id: str):
    # buscamos en la lista de películas la que tenga el mismo ID
    return next((m for m in movies_list if m ['id'] == id), {"detalle": "película no encontrada"})


# Ruta del chatbot que responde con películas segun palabras clave de la categoria
@app.get('/chatbot', tags=['chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intension del usuario
    query_words = word_tokenize(query.lower())
    # Buscamos sinonimos de las palabras clave para ampliar la busqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)

    # Filtramos la lista de peliculas buscando coinsidencias en la categoria
    results = [m for m in movies_list if any (s in m ['category'].lower() for s in synonyms)]

    # Si encontramos las peliculas, enviamos la lista de peliculas; sino, mostramos un mensaje de que no se encontraron coinsidencias

    return JSONResponse(content={
        "respuesta": "aqui tienes algunas peliculas relacionadas." if results else "no encontre peliculas en esa categoria.",
        "peliculas": results
    })


# Ruta para buscar películas por categoría específica
@app.get('/movies/by_category/', tags=['Movies'])
def get_movies_by_category(category: str):
    # Filtramos la lista de películas según la categoría ingresada
    return [m for m in movies_list if category.lower() in m ['category'].lower()]

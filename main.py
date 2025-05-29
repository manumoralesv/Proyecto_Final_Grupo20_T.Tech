# Importamos las herramientas necesarias para construir nuestra API
from fastapi import FastAPI, HTTPException  # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse  # HTMLResponse para paginas web, JSONResponse para respuestas en formato JSON
import pandas as pd  # Pandas es una herramienta para manejar datos en tablas.
import nltk  # NLTK es una herramienta para procesar texto y analizar palabras.
from fastapi.staticfiles import StaticFiles # Para servir archivos estáticos como CSS e imágenes.
from fastapi.templating import Jinja2Templates # Para renderizar plantillas HTML.
nltk.download('punkt_tab') # Herramienta para dividir frases en palabras.
nltk.download("punkt")  # Herramienta para dividir frases en palabras.
from nltk.tokenize import word_tokenize

# Funcion para cargar los datos desde un archivo CSV.
def load_data():
    # Leemos el archivo que contiene la informacion de las peliculas y seleccionamos las columnas importantes
    df = pd.read_csv("Dataset/Data.csv")

    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')


# Cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
#data_list = load_data()


# Creamos la aplicación FastAPI, que sera el motor de nuestra API.
# Esto inicializa la API con un nombre y una version.
app = FastAPI()

# Enlazamos la carpeta de archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enlazamos la carpeta de plantillas HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("templates/home.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())

# Ruta del chatbot
@app.get("/chatbot", response_class=HTMLResponse)
async def get_chatbot():
    with open("templates/chatbot.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


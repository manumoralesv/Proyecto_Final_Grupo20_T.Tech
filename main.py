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
from pydantic import BaseModel

# Funcion para cargar los datos desde un archivo CSV.
def load_data():
    # Leemos el archivo que contiene la informacion de las peliculas y seleccionamos las columnas importantes
    df = pd.read_csv("Dataset/Data.csv")

    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# Cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
# data_list = load_data()

# Creamos la aplicación FastAPI, que sera el motor de nuestra API.
# Esto inicializa la API con un nombre y una version.
app = FastAPI()

# Enlazamos la carpeta de archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enlazamos la carpeta de plantillas HTML
templates = Jinja2Templates(directory="templates")

user_name = {"name": None}


class NameRequest(BaseModel):
    name: str


@app.get("/", response_class=HTMLResponse, tags=["páginas"])
async def get_home():
    with open("templates/home.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.get("/chatbot", response_class=HTMLResponse, tags=["páginas"])
async def get_chatbot():
    with open("templates/chatbot.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.post("/set_name", tags=["chatbot"])
async def set_name(request: NameRequest):
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío.")
    user_name["name"] = request.name.strip()
    return {"message": f"¡Hola, {user_name['name']}! cómo estás, soy tu asistente virtual que te orientara sobre Energías Renovables. Escribe tu consulta:"}


@app.get("/chatbot/message", tags=["chatbot"])
async def use_chatbot(query: str):
    if not user_name["name"]:
        return JSONResponse(content={
            'respuesta': "Por favor, primero ingresa tu nombre para comenzar."
        })

    consulta = query.lower()
    return JSONResponse(content={
        'respuesta': f"{user_name['name']}, estoy procesando tu pregunta: {consulta}"
    })

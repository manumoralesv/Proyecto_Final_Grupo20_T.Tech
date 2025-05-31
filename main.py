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
#Datos de el csv: Departamento;Precio Panel Individual (COP);Costo Sistema Residencial (COP);Costo Sistema Comercial (COP);Notas

# Funcion para cargar los datos desde un archivo CSV.
def load_data():
    # Leemos el archivo que contiene la informacion de los paneles solares y seleccionamos las columnas importantes
    df = pd.read_csv("Dataset/Data.csv", delimiter= ";", encoding='utf-8')

    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# Cargamos los datos al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
data_list = load_data()

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
    return {"message": f"¡Hola, {user_name['name']}! cómo estás, soy tu asistente virtual que te orientará sobre Energías Renovables. Para ver las opciones disponibles escribe la palabra menu."}
    

@app.get("/chatbot/message", tags=["chatbot"])
async def use_chatbot(query: str):
    if not user_name["name"]:
        return JSONResponse(content={
            'respuesta': "Por favor, primero ingresa tu nombre para comenzar."
        })

    consulta = query.lower()
    data = [
        {"category": "1", "phrase": "¿Qué son los paneles solares?"},
        {"category": "1", "phrase": "¿Qué son las placas solares?"},
        {"category": "1", "phrase": "¿Qué son los modulos solares?"},
        {"category": "1", "phrase": "¿Para qué sirven los paneles solares?"},
        {"category": "1", "phrase": "¿Cuál es la función de un panel solar?"},
        {"category": "1", "phrase": "¿Me puedes explicar qué es un panel solar?"},
        {"category": "1", "phrase": "¿En qué consiste un panel solar?"},
        {"category": "2", "phrase": "¿Cómo funcionan los paneles solares?"},
        {"category": "2", "phrase": "¿De qué manera operan los paneles solares?"},
        {"category": "2", "phrase": "¿Cómo generan energía los paneles solares?"},
        {"category": "2", "phrase": "¿Cuál es el mecanismo de los paneles solares?"},
        {"category": "2", "phrase": "¿Cómo producen electricidad los paneles solares?"},
        {"category": "3", "phrase": "¿Qué tipos de paneles solares existen?"},
        {"category": "3", "phrase": "¿Cuáles son las clases de paneles solares?"},
        {"category": "3", "phrase": "¿Qué variedades de paneles solares hay?"},
        {"category": "3", "phrase": "¿Me puedes decir los tipos de paneles solares?"},
        {"category": "4", "phrase": "¿Qué beneficios presentan los paneles solares?"},
        {"category": "4", "phrase": "¿Cuáles son las ventajas de los paneles solares?"},
        {"category": "4", "phrase": "¿Por qué es bueno instalar paneles solares?"},
        {"category": "4", "phrase": "¿Qué aportan los paneles solares?"},
        {"category": "5", "phrase": "¿Cómo se instalan los paneles solares?"},
        {"category": "5", "phrase": "¿Cuál es el proceso para instalar paneles solares?"},
        {"category": "5", "phrase": "¿Qué pasos hay que seguir para instalar paneles solares?"},
        {"category": "5", "phrase": "¿Cómo puedo poner paneles solares en mi casa?"},
        {"category": "6", "phrase": "¿Qué mantenimiento requieren los paneles solares?"},
        {"category": "6", "phrase": "¿Cómo se cuidan los paneles solares?"},
        {"category": "6", "phrase": "¿Qué cuidados necesitan los paneles solares?"},
        {"category": "6", "phrase": "¿Cada cuánto hay que revisar los paneles solares?"},
        {"category": "7", "phrase": "¿Cuánto cuesta instalar paneles solares en mi departamento?"},
        {"category": "7", "phrase": "¿Cuál es el precio de los paneles solares para un departamento?"},
        {"category": "7", "phrase": "¿Qué valor tiene poner paneles solares en mi vivienda?"},
        {"category": "7", "phrase": "¿Cuánto debo invertir para instalar paneles solares?"},
        {"category": "8", "phrase": "¿Cuánto puedes ahorrar con paneles solares?"},
        {"category": "8", "phrase": "¿Qué ahorro ofrecen los paneles solares?"},
        {"category": "8", "phrase": "¿Cuánto dinero se ahorra con paneles solares?"},
        {"category": "8", "phrase": "¿En cuánto tiempo recupero la inversión de paneles solares?"},
        {"category": "9", "phrase": "¿Cómo impactan los paneles solares al medio ambiente?"},
        {"category": "9", "phrase": "¿Qué efecto tienen los paneles solares en el medio ambiente?"},
        {"category": "9", "phrase": "¿Los paneles solares ayudan al medio ambiente?"},
        {"category": "9", "phrase": "¿Cuál es el impacto ambiental de los paneles solares?"},
        {"category": "10", "phrase": "¿Dónde son más efectivos los paneles solares?"},
        {"category": "10", "phrase": "¿En qué lugares funcionan mejor los paneles solares?"},
        {"category": "10", "phrase": "¿Dónde conviene instalar paneles solares?"},
        {"category": "10", "phrase": "¿En qué zonas rinden más los paneles solares?"},
    ]
    
    responses = {
        "1": "Las placas solares son un dispositivo de captación de radiación solar y es capaz de transformarla en calor para el uso de aguas residenciales (colector solar) o en el electricidad para la alimentación de los consumos energéticos de una vivienda o comercio (panel solar fotovoltaico). Su fabricación se basa en células fotovoltaicas de silicio.",
        "2": "Los paneles solares funcionan convirtiendo la luz solar en electricidad. Utilizan células fotovoltaicas que generan corriente eléctrica cuando son expuestas a la luz solar.",
        "3": "Existen dos tipos principales de paneles solares: los paneles solares térmicos, que calientan agua, y los paneles solares fotovoltaicos, que generan electricidad.",
        "4": "Los paneles solares ofrecen varios beneficios, como la reducción de la factura de electricidad, la disminución de la huella de carbono y el aumento del valor de la propiedad.",
        "5": "La instalación de paneles solares implica colocar los paneles en un lugar adecuado, conectarlos al sistema eléctrico y asegurarse de que estén orientados correctamente para maximizar la captación de luz solar.",
        "6": "Los paneles solares requieren poco mantenimiento, pero es importante limpiarlos regularmente y revisar el sistema eléctrico para asegurarse de que todo funcione correctamente.",
        "8": "El ahorro con paneles solares depende del tamaño del sistema y el consumo de electricidad, pero muchos propietarios informan ahorros significativos en sus facturas mensuales.",
        "9": "Los paneles solares tienen un impacto ambiental positivo al reducir la dependencia de combustibles fósiles y disminuir las emisiones de gases de efecto invernadero.",
        "10": "Los paneles solares son más efectivos en áreas con alta exposición solar, como regiones soleadas y desérticas, pero también pueden funcionar en climas nublados.",
        }
    
    
    if consulta == "7":
        return await precios_dep()
    
    else:   
        return JSONResponse(content={
            'respuesta': f"""Encantada de ayudarte {user_name['name']}.
            {responses[consulta]}"""
        })

async def precios_dep():
    response = "Los precios de los paneles solares por departamento son:\n"
    for item in data_list:
        response += (
        f"\nDepartamento de {item['Departamento']}: "
            f"Individual {item['Precio Panel Individual (COP)']} COP, "
            f"Sistema residencial {item['Costo Sistema Residencial (COP)']} COP, "
            f"Sistema comercial {item['Costo Sistema Comercial (COP)']} COP\n"
        )
    return JSONResponse(content={
        'respuesta': response
    })
# Importamos las herramientas necesarias para construir nuestra API
from fastapi import FastAPI, HTTPException  # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse  # HTMLResponse para paginas web, JSONResponse para respuestas en formato JSON
import pandas as pd  # Pandas es una herramienta para manejar datos en tablas.
from fastapi.staticfiles import StaticFiles # Para servir archivos estáticos como CSS e imágenes.
from fastapi.templating import Jinja2Templates # Para renderizar plantillas HTML.
import spacy  # Spacy es una biblioteca de procesamiento de lenguaje natural.
from pydantic import BaseModel # Pydantic nos ayuda a definir modelos de datos y validar entradas.
from typing import List # Importamos List para definir tipos de listas.
import difflib  # Difflib nos ayuda a encontrar coincidencias entre cadenas de texto.
import sys
from typing import Union
#Datos de el csv: Departamento;Precio Panel Individual (COP);Costo Sistema Residencial (COP);Costo Sistema Comercial (COP);Notas

# Funcion para cargar los datos desde un archivo CSV.
def load_data():
    # Leemos el archivo que contiene la informacion de los paneles solares y seleccionamos las columnas importantes
    df = pd.read_csv("Dataset/Data.csv", delimiter= ";", encoding='utf-8')

    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# Cargamos los datos al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
data_list = load_data()

#definimos nuestra función de spacy en español
func = spacy.load("es_core_news_md")  # Cargamos el modelo de lenguaje español de Spacy.

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

#Creamos la lista de preguntas frecuentes y sus respuestas
# Esta lista contiene preguntas frecuentes sobre paneles solares, organizadas por categorías.
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
        {"category": "5", "phrase": "Instalar paneles solares"},
        {"category": "5", "phrase": "Poner paneles solares"},
        {"category": "5", "phrase": "Colocación de paneles solares"},
        {"category": "5", "phrase": "¿Cómo puedo poner paneles solares en mi casa?"},
        {"category": "6", "phrase": "¿Qué mantenimiento requieren los paneles solares?"},
        {"category": "6", "phrase": "¿Cómo se cuidan los paneles solares?"},
        {"category": "6", "phrase": "¿Qué cuidados necesitan los paneles solares?"},
        {"category": "6", "phrase": "¿Cada cuánto hay que revisar los paneles solares?"},
        {"category": "7", "phrase": "¿Cuánto cuesta un panel solar?"},
        {"category": "7", "phrase": "¿Cuánto vale un panel solar?"},
        {"category": "7", "phrase": "¿Cuánto cuesta instalar paneles solares?"},
        {"category": "7", "phrase": "¿Cuál es el precio de un panel solar?"},
        {"category": "7", "phrase": "¿Cuál es el valor de los paneles solares?"},
        {"category": "7", "phrase": "precio panel solar"},
        {"category": "7", "phrase": "cuánto cuesta"},
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
        {"category": "11", "phrase": "¿Existen subsidios para paneles solares en Colombia?"},
        {"category": "11", "phrase": "¿Hay ayudas gubernamentales para instalar paneles solares?"},
        {"category": "11", "phrase": "¿Cómo financiar paneles solares?"},
        {"category": "12", "phrase": "¿Cuánto duran los paneles solares?"},
        {"category": "12", "phrase": "¿Qué garantía tienen los paneles solares?"},
        {"category": "12", "phrase": "Vida útil de un panel solar"},
        {"category": "13", "phrase": "¿Los paneles solares funcionan con cualquier techo?"},
        {"category": "13", "phrase": "¿Puedo instalar paneles solares en un apartamento?"},
        {"category": "13", "phrase": "Requisitos para instalar paneles solares"},
        {"category": "14", "phrase": "¿Funcionan los paneles solares cuando está nublado?"},
        {"category": "14", "phrase": "¿Lluvia y paneles solares?"},
        {"category": "14", "phrase": "Eficiencia en climas húmedos"},
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
    "11": "En Colombia, existen programas de subsidios y financiación para paneles solares, como el 'Programa de Energización Rural' y líneas de crédito verde. Algunas alcaldías también ofrecen incentivos fiscales.",
    "12": "Los paneles solares tienen una vida útil de '25 a 30 años'. La mayoría incluyen garantías de 10 a 12 años para rendimiento (80% de eficiencia mínima).",
    "13": "Los paneles solares son compatibles con la mayoría de techos (inclinados o planos). En apartamentos, se requiere permiso de la copropiedad y espacio adecuado en áreas comunes.",
    "14": "Sí, los paneles solares funcionan en días nublados, aunque su eficiencia disminuye un '15-25%'. La lluvia incluso ayuda a limpiar la superficie de los paneles.",
    }

@app.get("/chatbot", response_class=HTMLResponse, tags=["páginas"])
async def get_chatbot():
    with open("templates/chatbot.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.post("/set_name", tags=["chatbot"])
async def set_name(request: NameRequest):
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío.")
    user_name["name"] = request.name.strip()
    return {"message": f"¡Hola, {user_name['name']}! cómo estás, soy tu asistente virtual que te orientará sobre Energías Renovables."}

# Verificamos la version de python para usar el tipo de dato str | None o Union[str, None]
if sys.version_info >= (3, 10):
    ReturnType = str | None
else:
    ReturnType = Union[str, None]


def encontrar_categoria(pregunta_usuario: str) -> ReturnType:
    pregunta_usuario = pregunta_usuario.lower().strip()

    # Primero buscar coincidencias con palabras clave importantes
    palabras_clave = {
        "Qué son": "1",
        "Que son": "1",
        "instal": "5",  # Para "instalar", "instalación", etc.
        "funcion": "2",
        "función": "2",
        "tipos": "3",
        "beneficios": "4",
        "manten": "6",  # Para "mantenimiento", "mantener"
        "precio": "7",
        "cuesta": "7",
        "ahorr": "8",
        "medio ambiente": "9",
        "efectiv": "10", # Para "efectividad", "efectivo"
        "subsidio": "11",
        "financiacion": "11",
        "financiación": "11",
        "ayuda": "11",
        "credito": "11",
        "crédito": "11",
        "dura": "12",
        "vida util": "12",
        "garantia": "12",
        "garantía": "12",
        "techo": "13",
        "apartamento": "13",
        "edificio": "13",
        "nublado": "14",
        "lluvia": "14",
        "clima": "14",
        "invierno": "14",
        }
    
    for palabra, categoria in palabras_clave.items():
        if palabra in pregunta_usuario:
            return categoria
    
    # Luego buscar coincidencias exactas
    for item in data:
        if item["phrase"].lower() in pregunta_usuario or pregunta_usuario in item["phrase"].lower():
            return item["category"]
    
    # Finalmente usar spaCy con umbral más bajo
    doc_usuario = func(pregunta_usuario)
    mejor_score = 0
    mejor_categoria = None

    for item in data:
        doc_frase = func(item["phrase"].lower())
        score = doc_usuario.similarity(doc_frase)
        if score > mejor_score:
            mejor_score = score
            mejor_categoria = item["category"]

    return mejor_categoria if mejor_score >= 0.6 else None  # Bajamos el umbral a 0.65

@app.get("/chatbot/message", tags=["chatbot"])
async def use_chatbot(query: str):
    if not user_name["name"]:
        return JSONResponse(content={
            'respuesta': "Por favor, primero ingresa tu nombre para comenzar."
        })

    categoria = encontrar_categoria(query)

    if not categoria:
        # Buscar preguntas que contengan palabras similares a la consulta
        palabras_consulta = query.lower().split()
        sugerencias = []
        
        for item in data:
            if any(palabra in item["phrase"].lower() for palabra in palabras_consulta):
                if item["phrase"] not in sugerencias and len(sugerencias) < 3:
                    sugerencias.append(item["phrase"])
        
        # Si no encontramos sugerencias relacionadas, mostrar preguntas generales
        if not sugerencias:
            sugerencias = [item["phrase"] for item in data[:3]]
        
        return {
            "respuesta": f"Lo siento, no entendí tu pregunta. ¿Podrías reformularla?\n\n"
                        f"Algunas preguntas relacionadas que puedo responder:\n- " + 
                        "\n- ".join(sugerencias)
        }

    if categoria == "7":
        return await precios_dep(query)  # Pasar la consulta a la función de precios 

    respuesta = responses.get(categoria, "Lo siento, no tengo una respuesta para eso.")
    return {"respuesta": respuesta}

async def precios_dep(query: str = None):
    if query:
        # Buscar el departamento en la consulta
        departamento_encontrado = None
        for item in data_list:
            if item['Departamento'].lower() in query.lower():
                departamento_encontrado = item
                break
        
        if departamento_encontrado:
            response = (
                f"Precios en el departamento de {departamento_encontrado['Departamento']}:\n"
                f"Panel Individual: {departamento_encontrado['Precio Panel Individual (COP)']} COP\n"
                f"Sistema Residencial: {departamento_encontrado['Costo Sistema Residencial (COP)']} COP\n"
                f"Sistema Comercial: {departamento_encontrado['Costo Sistema Comercial (COP)']} COP"
            )
            return JSONResponse(content={'respuesta': response})
    
    # Si no se especificó un departamento o no se encontró, mostrar todos
    response = "Los precios de los paneles solares por departamento son:\n"
    for item in data_list:
        response += (
            f"\nDepartamento de {item['Departamento']}: "
            f"Individual {item['Precio Panel Individual (COP)']} COP, "
            f"Sistema residencial {item['Costo Sistema Residencial (COP)']} COP, "
            f"Sistema comercial {item['Costo Sistema Comercial (COP)']} COP"
        )
    return JSONResponse(content={'respuesta': response})
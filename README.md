# 🚀 SolarAPI - Asistente Virtual para Paneles Solares

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)

API de consulta inteligente sobre paneles solares, que cuenta con un chatbot integrado el cual tiene la función de asesorar sobre paneles solares en colombia. Este cuenta con un documento con datos de costos por departamento en Colombia y preguntas con respuestas pre-determinadas para crear un ambiente interactivo.

## 📌 Características principales

- **Chatbot interactivo**: Responde preguntas sobre paneles solares usando NLP (spaCy).
- **Interfaz web**: HTML/CSS responsive con diseño moderno.
- **Categorización automática**: Clasifica preguntas en 14 categorías temáticas pre-estabelcidas.

## 💻 Organización del repositorio
- **Dataset**: Carpeta en la que se encuentra el archivo CSV que contiene los datos usados de los precios en Colombia
- **static**: Carpeta que cuenta con todos los recursos decorativos como icono de la página o los archivos .css usados para la estética de la API
- **templates**: Carpeta que cuenta con los archivos .html usados para las ventanas independientes de home y chatbot.
- **main.py**: Archivo .py el cual cuenta con la estructura prinicpal de creación y uso de la API
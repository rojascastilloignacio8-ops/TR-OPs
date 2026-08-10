from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


personas = [
    { "nombre": "Jorge", "edad": 30 },
    { "nombre": "Juan", "edad": 31 },
    { "nombre": "Ricardo", "edad": 45 }
]

app = FastAPI()

class Persona(BaseModel):
    id: int
    nombre: str
    edad: int

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return { "Estado": "Servidor en línea"}

@app.get("/personas")
async def obtenerPersonas(limit: int = 10) -> list[Persona]:
    
    conexion = sqlite3.connect("liceo.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()
    respuesta = cursor.execute(f"SELECT * FROM personas LIMIT {limit}")
    return [dict(persona) for persona in respuesta.fetchall()]

@app.post("/personas")
async def agregarPersona(persona: Persona):
    # Escribe tu código aquí debajo
    personas.append(persona)
    return personas
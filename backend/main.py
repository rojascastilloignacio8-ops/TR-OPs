from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

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

# MODELOS
class Factura(BaseModel):
    id: int | None = None
    num_factura: int
    fecha: str
    cliente: str
    total: int

class facturaCreate(BaseModel):
    num_factura: int
    fecha: str
    cliente: str
    total: int
class facturaActual(BaseModel):
    total: int

#Productos
class Producto(BaseModel):
    id: int | None = None
    nombre: str
    precio: int
    stock: int
class eliminarProduct(BaseModel):
    id: int

# ENDPOINTS
# GET
    ##@app.get("/facturas")
    #async def obtenerFacturas()-> list[Factura]:
       # conexion = sqlite3.connect("./master.db")
       # conexion.row_factory = sqlite3.Row
       # cursor = conexion.cursor()
       # respuesta = cursor.execute("SELECT * FROM facturas ORDER BY fecha DESC")
       # facturas = respuesta.fetchall()
       # return [dict(factura) for factura in facturas]

@app.get("/facturas/{id}")
async def actualFactura(id: int):
    conexion = sqlite3.connect("./master.db")
    cursor = conexion.cursor()
    verifica = cursor.execute("SELECT * FROM facturas WHERE EXISTS (SELECT * FROM facturas WHERE id = ?) AND id = ?", (id, id, ))
    final = verifica.fetchall()
    if final == []:
        return "Producto no encontrado"
    conexion.commit()
    conexion.close()
    return final
# POST
@app.post("/facturas")
async def agregarFactura(factura: facturaCreate):
    conexion = sqlite3.connect("./master.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO facturas (numero_factura, fecha, cliente, total) VALUES (?, ?, ?, ?)", (factura.num_factura, factura.fecha, factura.cliente, factura.total))
    conexion.commit()
    conexion.close()
    return "Igresado Con Exito"
# PATCH

# PUT
@app.put("/facturas/{id}")
async def actualizaFact(id: int, actualFac: facturaActual):
    conexion = sqlite3.connect("./master.db")
    cursor = conexion.cursor()
    verifica = cursor.execute("SELECT * FROM facturas WHERE EXISTS (SELECT * FROM facturas WHERE id = ?) AND id = ?", (id, id, ))
    final = verifica.fetchone()
    if final == [] or final == None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cursor.execute("UPDATE facturas SET total=? WHERE id=?", (actualFac.total, id))
    conexion.commit()
    conexion.close()
    return "Actualizado Con Exito"
# DELETE
@app.delete("/facturas/{id}")
async def borrarfact(id: int):
    conexion = sqlite3.connect("./master.db")
    cursor = conexion.cursor()
    verifica = cursor.execute("SELECT * FROM facturas WHERE id=?", (id, ))
    final = verifica.fetchone()
    if final == [] or final == None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cursor.execute("DELETE FROM facturas WHERE id=?", (id, ))

#Productos
@app.get("/productos")
async def obtenerProductos()->list[Producto]:
    conexion = sqlite3.connect("./master.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    respuesta = cursor.execute("SELECT * FROM productos")
    productos = respuesta.fetchall()
    conexion.close()
    return [dict(producto) for producto in productos]

@app.delete("/productos/{id}")
async def eliminarProducto(id: int):
    conexion = sqlite3.connect("./master.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id, ))
    conexion.commit()
    conexion.close()
    return "Eliminado correctamente"
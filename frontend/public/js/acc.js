const boton = document.getElementById("traer-pro")
const tabla_cuerpo = document.getElementById("datos")
const cont_error = document.getElementById("cont-error")
function paraErrores(mensaje_error){
    cont_error.innerText = ""
    const text_error = document.createElement("h3")
    text_error.innerText = mensaje_error
    text_error.classList.add("errores")
    cont_error.appendChild(text_error)
}
async function eliminarProducto(id){
    try{
        const url = `http://localhost:8000/productos/${id}`
        const respuesta = await fetch(url,{
            method: "DELETE",
            headers:{"Content-Type":"application/json"},
        })
        if (!respuesta.ok){
            throw new Error(`Response status: ${respuesta.status}`)
        }
    } catch (error){
        console.error(error)
    }
}
async function construirProductos() {
    const url = "http://localhost:8000/productos"
    try{
        const respuesta = await fetch(url)
        if (!respuesta.ok){
            throw new Error(`Response status: ${respuesta.status}`)
        }
        cont_error.innerText = ""
        const resusltado = await respuesta.json()
        if (resusltado.length > 0){
            tabla_cuerpo.innerText = ""
            resusltado.forEach(producto => {
                const fila = document.createElement("tr")
                const dato_id = document.createElement("td")
                const dato_1 = document.createElement("td")
                const dato_2 = document.createElement("td")
                const dato_3 = document.createElement("td")
                const btn_eli = document.createElement("button")
                btn_eli.classList.add("btn-elimi")
                btn_eli.innerText = "Eliminar"
                dato_id.innerText = producto.id
                dato_1.innerText = producto.nombre
                dato_2.innerText = producto.precio
                dato_3.innerText = producto.stock
                fila.appendChild(dato_id)
                fila.appendChild(dato_1)
                fila.appendChild(dato_2)
                fila.appendChild(dato_3)
                fila.appendChild(btn_eli)
                tabla_cuerpo.appendChild(fila)
                btn_eli.addEventListener("click", (event)=>{
                    eliminarProducto(producto.id)    
                })
            });
        }
        console.log(resusltado)
    } catch (error){
        console.error(error)
        paraErrores(error)
    }
}
boton.addEventListener("click", async (event)=> {
    construirProductos()
})
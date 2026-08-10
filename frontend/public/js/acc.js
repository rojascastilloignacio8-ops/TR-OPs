const formulario = document.getElementById("formulario")
const caj = document.getElementById("cav")
const bot = document.getElementById("env")

const nombre = document.getElementById("nombre")
const edad = document.getElementById("edad")
const validaciones = {
    "nombre":{
        "mensaje": "Solo se aceptan letras, NO numeros ni caracteres especiales",
        "valida": /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$/
    }
}

formulario.addEventListener("submit", (event) => {
    event.preventDefault()

    console.log(nombre.value)
    console.log(edad.value)
    caj.innerHTML = ""
    agregarPersona(nombre.value, edad.value)
})
nombre.addEventListener("keyup", (event)=>{
    validacion("nombre", nombre.value)
})
function validacion(input_id, valor){
    const error_var = document.getElementById(`error-${input_id}`)
    if (!validaciones[input_id].valida.test(valor)){
        error_var.innerText = validaciones[input_id].mensaje
        bot.disabled = true
    } else{
        bot.disabled = false
        error_var.innerText = ""
    }
}

// 1.
// Definir una funcion llamada obtenerPersonas que envíe una petición fetch hacia el servidor
// y con el resultado construir una interfaz para mostrar a las personas.
async function obtenerPersonas(){

    const url = "http://localhost:8000/personas"

    try{
        const respuesta = await fetch(url)
        if (!respuesta.ok){
            throw new Error(`Response status: ${respuesta.status};
            }`)
        }
        const resultado = await respuesta.json()
        construirInterfaz(resultado)
    }catch (error) {
        console.error(error)
    }
}
obtenerPersonas()

// 2.
// Definir una función llamada agregarPersona que envíe una petición fetch de tipo POST hacia el servidor
// con los datos escritos en el formulario.
async function agregarPersona(nombre, edad){
    const url = "http://localhost:8000/personas"

    try{
        const respuesta = await fetch(url, {
            method: "POST",
            headers:{"Content-Type": "application/json"},
            body: JSON.stringify({"nombre": nombre, "edad": edad}),
        })
        if (!respuesta.ok){
            throw new Error(`Response status: ${respuesta.status}`)
        }
        const resultado = await respuesta.json()
        construirInterfaz(resultado)
    }catch (error) {
        console.error(error)
    }
}
function construirInterfaz(personas){
    personas.forEach(persona => {
        let tex = document.createElement("h4")
        let dif = document.createElement("div")
        tex.innerText = `Nombre: ${persona.nombre} \n Edad: ${persona.edad}`
        dif.appendChild(tex)
        caj.appendChild(dif)
    });
}
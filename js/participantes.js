document.addEventListener("DOMContentLoaded", function () {

    const botonGenerar = document.getElementById("boton-generar");
    const contenedor = document.getElementById("contenedor-participantes");
    const inputCantidad = document.getElementById("cantidadParticipantes");
    const mensaje = document.getElementById("mensaje-cantidad");

    botonGenerar.addEventListener("click", function () {

        contenedor.innerHTML = "";
        mensaje.textContent = "";

        const cantidad = parseInt(inputCantidad.value);

        if (!cantidad || cantidad < 1 || cantidad > 10) {
            mensaje.textContent = "Ingrese una cantidad de participantes entre 1 y 10";
            return;
        }

        const campos = [
            { etiqueta: "Apellido y Nombre", tipo: "text" },
            { etiqueta: "DNI", tipo: "text" },
            { etiqueta: "Fecha de nacimiento", tipo: "date" },
            { etiqueta: "Sexo", tipo: "text" },
            { etiqueta: "Nivel", tipo: "text" }
        ];

        for (let i = 1; i <= cantidad; i++) {

            const seccion = document.createElement("section");
            seccion.classList.add("bloque-participante");

            const titulo = document.createElement("h3");
            titulo.textContent = "Participante " + i;
            seccion.appendChild(titulo);

            campos.forEach(function (campo) {

                const idCampo = campo.etiqueta.toLowerCase().replace(/ /g, "-") + "-" + i;

                const label = document.createElement("label");
                label.setAttribute("for", idCampo);
                label.textContent = campo.etiqueta + ":";

                const input = document.createElement("input");
                input.setAttribute("type", campo.tipo);
                input.setAttribute("id", idCampo);
                input.setAttribute("name", idCampo);

                seccion.appendChild(label);
                seccion.appendChild(input);
            });

            contenedor.appendChild(seccion);
        }
    });
});

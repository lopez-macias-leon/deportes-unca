document.addEventListener("DOMContentLoaded", function () {

    const formulario = document.getElementById("formulario-inscripcion");

    if (!formulario) {
        return;
    }

    formulario.addEventListener("submit", function (evento) {

        let esValido = true;

        const inputFecha = document.getElementById("fecha_nacimiento");
        const mensajeFecha = document.getElementById("mensaje-fecha");

        const fechaIngresada = new Date(inputFecha.value);
        const fechaActual = new Date();

        if (inputFecha.value !== "" && fechaIngresada > fechaActual) {
            mensajeFecha.textContent = "La fecha de nacimiento no puede ser posterior a la fecha actual";
            esValido = false;
        } else {
            mensajeFecha.textContent = "";
        }

        const inputDni = document.getElementById("dni");
        const mensajeDni = document.getElementById("mensaje-dni");

        const patronDni = /^[0-9]{8}$/;

        if (!patronDni.test(inputDni.value)) {
            mensajeDni.textContent = "El DNI debe contener 8 dígitos";
            esValido = false;
        } else {
            mensajeDni.textContent = "";
        }

        if (!esValido) {
            evento.preventDefault();
        }
    });
});

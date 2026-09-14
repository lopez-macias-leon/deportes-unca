function Actividad(nombre, lugar, dia, horario, cupo, estado) {
    this.nombre = nombre;
    this.lugar = lugar;
    this.dia = dia;
    this.horario = horario;
    this.cupo = cupo;
    this.estado = estado;
}

class SistemaDeportes {
    constructor() {
        this.actividades = [];
    }

    agregarActividad(actividad) {
        this.actividades.push(actividad);
    }

    listarActividades() {
        return this.actividades;
    }
}

const sistemaDeportes = new SistemaDeportes();

sistemaDeportes.agregarActividad(
    new Actividad("Fútbol", "Cancha Universitaria", "Lunes", "18:00 - 20:00", 20, "Disponible")
);
sistemaDeportes.agregarActividad(
    new Actividad("Básquet", "Cancha Techada", "Martes", "17:00 - 19:00", 15, "Disponible")
);
sistemaDeportes.agregarActividad(
    new Actividad("Vóley", "Cancha Techada", "Miércoles", "18:00 - 20:00", 12, "Completo")
);
sistemaDeportes.agregarActividad(
    new Actividad("Atletismo", "Pista de Atletismo", "Jueves", "16:00 - 18:00", 25, "Disponible")
);

document.addEventListener("DOMContentLoaded", function () {

    const cuerpoTabla = document.getElementById("cuerpoTabla");

    if (!cuerpoTabla) {
        return;
    }

    const actividades = sistemaDeportes.listarActividades();

    actividades.forEach(function (actividad) {

        const fila = document.createElement("tr");

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = actividad.nombre;

        const celdaLugar = document.createElement("td");
        celdaLugar.textContent = actividad.lugar;

        const celdaDia = document.createElement("td");
        celdaDia.textContent = actividad.dia;

        const celdaHorario = document.createElement("td");
        celdaHorario.textContent = actividad.horario;

        const celdaCupo = document.createElement("td");
        celdaCupo.textContent = actividad.cupo;

        const celdaEstado = document.createElement("td");
        celdaEstado.textContent = actividad.estado;

        if (actividad.estado === "Completo") {
            celdaEstado.classList.add("estado-completo");
        } else {
            celdaEstado.classList.add("estado-activa");
        }

        fila.appendChild(celdaNombre);
        fila.appendChild(celdaLugar);
        fila.appendChild(celdaDia);
        fila.appendChild(celdaHorario);
        fila.appendChild(celdaCupo);
        fila.appendChild(celdaEstado);

        cuerpoTabla.appendChild(fila);
    });
});

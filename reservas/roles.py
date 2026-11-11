"""Roles de usuario de Deportes UNCA.

Cada rol es un Grupo de Django con un conjunto de permisos sobre
ActividadDeportiva. Los grupos se crean automáticamente con la migración
0003_crear_roles.

- Administrador: gestión completa (ver, agregar, modificar y eliminar).
- Coordinador:   ver, agregar y modificar actividades (no puede eliminar).
- Socio:         solo puede ver las actividades.
"""

ADMINISTRADOR = "Administrador"
COORDINADOR = "Coordinador"
SOCIO = "Socio"

PERMISOS_POR_ROL = {
    ADMINISTRADOR: ["view", "add", "change", "delete"],
    COORDINADOR: ["view", "add", "change"],
    SOCIO: ["view"],
}

# TP VIII - Admin de Django | Deportes UNCA

Programación III · Ingeniería en Informática · FTyCA – UNCA
Alumno: Lopez Macias Leon (MU 01949) · Rama: `tp8-django`

Proyecto "Deportes UNCA" (continuación del TP VII) con el panel de administración de Django configurado, medidas de seguridad y autenticación basada en roles.

## Instalación y ejecución

Requiere Python 3.10 o superior.

```bash
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Linux/macOS
pip install -r requirements.txt
python manage.py migrate         # crea las tablas y los roles
python manage.py runserver
```

- Sitio: http://127.0.0.1:8000/actividades/ (pide iniciar sesión)
- Admin: http://127.0.0.1:8000/admin/

## Consignas

### 1) Superusuario

```bash
python manage.py createsuperuser
```

Se ingresa usuario, email y contraseña (la contraseña tiene que pasar los validadores: mínimo 8 caracteres, no común, no solo numérica). Con ese usuario se entra a `/admin/`.

### 2) Registro del modelo en el Admin

En `reservas/admin.py` el modelo `ActividadDeportiva` se registra con el decorador `@admin.register(ActividadDeportiva)` y una clase `ActividadDeportivaAdmin`.

### 3) Listar, crear, actualizar y eliminar

Desde *Reservas → Actividades deportivas* se puede ver el listado, agregar con **Agregar actividad deportiva**, entrar a un registro para modificarlo y eliminarlo con **Eliminar** (o con la acción "Eliminar seleccionados" del listado). Las capturas están en [`docs/capturas/`](docs/capturas/).

### 4) `list_display` y `search_fields`

```python
@admin.register(ActividadDeportiva)
class ActividadDeportivaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "lugar", "cupo")
    search_fields = ("nombre", "lugar", "descripcion")
    list_filter = ("lugar",)
    list_display_links = ("id", "nombre")
    ordering = ("nombre",)
    list_per_page = 20
```

- `list_display`: columnas que muestra el listado.
- `search_fields`: habilita la barra de búsqueda por nombre, lugar o descripción (por ejemplo, buscar "gimnasio").
- Además se agregó un filtro lateral por lugar y títulos personalizados del panel.

## Seguridad aplicada

| Técnica | Dónde |
|---|---|
| `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` se leen de variables de entorno (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`) | `settings.py` |
| Validadores de contraseña activados (longitud mínima, similitud con el usuario, contraseñas comunes, solo numéricas) | `settings.py` |
| Protección CSRF: `CsrfViewMiddleware` y `{% csrf_token %}` en todos los formularios; eliminar y cerrar sesión solo por POST | middleware, templates, `@require_POST` |
| Clickjacking: `X_FRAME_OPTIONS = "DENY"` | `settings.py` |
| Cookies `HttpOnly`, sesión que vence en 1 hora y al cerrar el navegador | `settings.py` |
| `SECURE_CONTENT_TYPE_NOSNIFF` y `SECURE_REFERRER_POLICY` | `settings.py` |
| Con `DEBUG=False`: cookies solo por HTTPS, redirección a HTTPS y HSTS | `settings.py` |
| XSS: los templates escapan automáticamente las variables | templates |
| Inyección SQL: todas las consultas usan el ORM de Django | `views.py` |
| Validación del lado del servidor: el cupo debe ser mayor que cero (en el formulario y en el modelo) | `forms.py`, `models.py` |
| Todas las vistas exigen sesión iniciada (`@login_required`) y el permiso del rol (`@permission_required`, responde 403) | `views.py` |

Verificación para producción:

```bash
DJANGO_DEBUG=False DJANGO_SECRET_KEY=<clave-larga> python manage.py check --deploy
```

## Autenticación basada en roles

Los roles son **Grupos** de Django con permisos sobre `ActividadDeportiva`. Se crean solos al ejecutar `migrate` (migración `0003_crear_roles`).

| Rol | Ver | Agregar | Modificar | Eliminar | Entra al Admin |
|---|:-:|:-:|:-:|:-:|:-:|
| Administrador | ✔ | ✔ | ✔ | ✔ | ✔ |
| Coordinador | ✔ | ✔ | ✔ | ✖ | ✔ (solo lo que su rol permite) |
| Socio | ✔ | ✖ | ✖ | ✖ | ✖ |

Crear usuarios con un rol (la contraseña se pide por teclado):

```bash
python manage.py crear_usuario_rol coordinador Coordinador
python manage.py crear_usuario_rol socio Socio
```

También se pueden crear desde el Admin (*Usuarios → Agregar* y asignarles un grupo).

En el sitio, el menú y los botones (Agregar, Editar, Eliminar) aparecen según los permisos del usuario, y si alguien intenta entrar por URL a una acción que su rol no permite, recibe "Acceso denegado (403)". Rutas:

- `/cuentas/login/` y cierre de sesión
- `/actividades/`, `/actividades/<id>/`
- `/actividades/agregar/`, `/actividades/<id>/editar/`, `/actividades/<id>/eliminar/`

## Tests

```bash
python manage.py test reservas
```

Comprueban los roles, los permisos de cada uno, la redirección al login, la validación del cupo y la configuración y búsqueda del Admin.

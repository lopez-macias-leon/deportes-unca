# TP VII - Vistas y Templates en Django | Deportes UNCA

Implementación de las tres consignas del Trabajo Práctico VII de Programación III.

## Estructura

- `manage.py`: comando de administración de Django.
- `deportes/settings.py`: configuración del proyecto y SQLite.
- `deportes/urls.py`: incluye las rutas de la aplicación `reservas`.
- `reservas/models.py`: modelo `ActividadDeportiva`.
- `reservas/forms.py`: formulario basado en `ModelForm`.
- `reservas/views.py`: vistas para agregar, listar y ver el detalle.
- `reservas/urls.py`: rutas `/actividades/`, `/actividades/agregar/` y `/actividades/<id>/`.
- `reservas/templates/reservas/`: templates solicitados.

## Instalación y ejecución

Requiere Python 3.10 o superior.

```bash
python -m venv venv
```

Activar el entorno virtual:

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Instalar Django:

```bash
pip install -r requirements.txt
```

Crear las tablas de SQLite:

```bash
python manage.py makemigrations reservas
python manage.py migrate
```

Ejecutar el servidor:

```bash
python manage.py runserver
```

Abrir en el navegador:

- Listado: http://127.0.0.1:8000/actividades/
- Agregar: http://127.0.0.1:8000/actividades/agregar/
- Detalle: http://127.0.0.1:8000/actividades/1/

## Cómo se resuelven las consignas

1. `agregar_actividad`: muestra el formulario en GET. En POST valida con `is_valid()`, guarda con `save()` y muestra un mensaje mediante `messages.success`.
2. `lista_actividades`: consulta todos los registros con `ActividadDeportiva.objects.all()` y los envía al template mediante el contexto.
3. `detalle_actividad`: recibe `id` desde la URL y busca el registro con `get_object_or_404`, que responde 404 si no existe.

El formulario utiliza `method="post"` y `{% csrf_token %}`. Las vistas son funciones y las consultas se realizan con el ORM de Django.

## Integración en el proyecto existente

El repositorio público consultado contiene actualmente archivos HTML estáticos (`pagina1.html`, `pagina2.html` e `inscripciones.html`) en la rama `tp1-html5`; no aparece allí un proyecto Django ni una aplicación `reservas`. Por eso este ZIP incluye una estructura Django mínima y funcional para el TP. Si ya tenés el proyecto Django de la cátedra en otra carpeta o rama, podés copiar `models.py`, `forms.py`, `views.py`, `urls.py` y `templates/reservas/` a la aplicación `reservas`, y agregar `reservas` a `INSTALLED_APPS`.

En el proyecto real, si `ActividadDeportiva` ya existe, conservá ese modelo y adaptá solamente los nombres de campos si fueran diferentes. No dupliques el modelo.

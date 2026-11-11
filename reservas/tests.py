from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .admin import ActividadDeportivaAdmin
from .models import ActividadDeportiva


class RolesYPermisosTest(TestCase):
    def setUp(self):
        self.actividad = ActividadDeportiva.objects.create(
            nombre="Fútbol", descripcion="Fútbol 5", lugar="Polideportivo", cupo=10
        )
        self.usuarios = {}
        for rol in ["Administrador", "Coordinador", "Socio"]:
            usuario = User.objects.create_user(rol.lower(), password="ClaveSegura.2026")
            usuario.groups.add(Group.objects.get(name=rol))
            self.usuarios[rol] = usuario

    def url(self, nombre, *args):
        return reverse(f"reservas:{nombre}", args=args)

    def test_los_roles_existen(self):
        self.assertEqual(
            set(Group.objects.values_list("name", flat=True)),
            {"Administrador", "Coordinador", "Socio"},
        )

    def test_anonimo_es_redirigido_al_login(self):
        respuesta = self.client.get(self.url("lista_actividades"))
        self.assertRedirects(respuesta, f"{reverse('login')}?next=/actividades/")

    def test_socio_solo_puede_ver(self):
        self.client.force_login(self.usuarios["Socio"])
        self.assertEqual(self.client.get(self.url("lista_actividades")).status_code, 200)
        self.assertEqual(self.client.get(self.url("detalle_actividad", self.actividad.id)).status_code, 200)
        self.assertEqual(self.client.get(self.url("agregar_actividad")).status_code, 403)
        self.assertEqual(self.client.get(self.url("editar_actividad", self.actividad.id)).status_code, 403)
        self.assertEqual(self.client.post(self.url("eliminar_actividad", self.actividad.id)).status_code, 403)

    def test_coordinador_agrega_y_edita_pero_no_elimina(self):
        self.client.force_login(self.usuarios["Coordinador"])
        datos = {"nombre": "Vóley", "descripcion": "Mixto", "lugar": "Gimnasio", "cupo": 12}
        self.client.post(self.url("agregar_actividad"), datos)
        self.assertTrue(ActividadDeportiva.objects.filter(nombre="Vóley").exists())
        self.assertEqual(self.client.get(self.url("editar_actividad", self.actividad.id)).status_code, 200)
        self.assertEqual(self.client.post(self.url("eliminar_actividad", self.actividad.id)).status_code, 403)

    def test_administrador_puede_eliminar(self):
        self.client.force_login(self.usuarios["Administrador"])
        self.client.post(self.url("eliminar_actividad", self.actividad.id))
        self.assertFalse(ActividadDeportiva.objects.filter(pk=self.actividad.id).exists())

    def test_cupo_debe_ser_positivo(self):
        self.client.force_login(self.usuarios["Administrador"])
        datos = {"nombre": "Básquet", "descripcion": "x", "lugar": "y", "cupo": 0}
        self.client.post(self.url("agregar_actividad"), datos)
        self.assertFalse(ActividadDeportiva.objects.filter(nombre="Básquet").exists())


class AdminTest(TestCase):
    def setUp(self):
        self.superusuario = User.objects.create_superuser("admin", password="ClaveSegura.2026")
        ActividadDeportiva.objects.create(nombre="Natación", descripcion="Libre", lugar="Pileta", cupo=20)
        ActividadDeportiva.objects.create(nombre="Tenis", descripcion="Singles", lugar="Canchas", cupo=4)

    def test_modelo_registrado_con_personalizacion(self):
        model_admin = admin.site._registry[ActividadDeportiva]
        self.assertIsInstance(model_admin, ActividadDeportivaAdmin)
        self.assertEqual(model_admin.list_display, ("id", "nombre", "lugar", "cupo"))
        self.assertEqual(model_admin.search_fields, ("nombre", "lugar", "descripcion"))

    def test_busqueda_en_el_admin(self):
        self.client.force_login(self.superusuario)
        url = reverse("admin:reservas_actividaddeportiva_changelist")
        respuesta = self.client.get(url, {"q": "pileta"})
        self.assertContains(respuesta, "Natación")
        self.assertNotContains(respuesta, "Tenis")

    def test_socio_no_entra_al_admin(self):
        socio = User.objects.create_user("socio", password="ClaveSegura.2026")
        self.client.force_login(socio)
        respuesta = self.client.get(reverse("admin:index"))
        self.assertEqual(respuesta.status_code, 302)

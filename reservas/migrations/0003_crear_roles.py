from django.contrib.auth.management import create_permissions
from django.db import migrations

PERMISOS_POR_ROL = {
    "Administrador": ["view", "add", "change", "delete"],
    "Coordinador": ["view", "add", "change"],
    "Socio": ["view"],
}


def crear_roles(apps, schema_editor):
    # Los permisos se crean recién al final de "migrate"; los forzamos acá
    # para poder asignarlos a los grupos.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for rol, acciones in PERMISOS_POR_ROL.items():
        grupo, _ = Group.objects.get_or_create(name=rol)
        permisos = Permission.objects.filter(
            content_type__app_label="reservas",
            codename__in=[f"{accion}_actividaddeportiva" for accion in acciones],
        )
        grupo.permissions.set(permisos)


def eliminar_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=PERMISOS_POR_ROL.keys()).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("reservas", "0002_cupo_minimo"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [migrations.RunPython(crear_roles, eliminar_roles)]

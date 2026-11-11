from getpass import getpass

from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from reservas.roles import PERMISOS_POR_ROL


class Command(BaseCommand):
    help = "Crea un usuario y le asigna un rol (Administrador, Coordinador o Socio)."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("rol", choices=list(PERMISOS_POR_ROL))
        parser.add_argument("--password", help="Si no se indica, se pide por teclado.")

    def handle(self, *args, username, rol, password=None, **options):
        if User.objects.filter(username=username).exists():
            raise CommandError(f'El usuario "{username}" ya existe.')

        password = password or getpass("Contraseña: ")
        usuario = User(username=username, is_staff=(rol != "Socio"))
        try:
            validate_password(password, usuario)
        except ValidationError as error:
            raise CommandError(" ".join(error.messages))

        usuario.set_password(password)
        usuario.save()
        usuario.groups.add(Group.objects.get(name=rol))
        self.stdout.write(self.style.SUCCESS(f'Usuario "{username}" creado con rol {rol}.'))

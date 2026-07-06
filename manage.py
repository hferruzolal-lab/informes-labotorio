#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    usuario, creado = User.objects.get_or_create(username=username)

    usuario.email = email or ""
    usuario.is_staff = True
    usuario.is_superuser = True
    usuario.set_password(password)
    usuario.save()

    print("Superusuario listo:", username)
else:
    print("No se creó superusuario porque faltan variables de entorno.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

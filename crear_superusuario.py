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
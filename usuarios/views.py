from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CorreoForm, CodigoForm, NuevaPasswordForm
from .models import CodigoRecuperacion
import random
from django.core.mail import send_mail
from django.conf import settings


def recuperar_password(request):
    if request.method == "POST":
        form = CorreoForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data["correo"]

            if not User.objects.filter(email=correo).exists():
                form.add_error(
                    "correo",
                    "No existe una cuenta registrada con ese correo."
                )

                return render(request, "usuarios/recuperar.html", {
                    "form": form
                })

            codigo = str(random.randint(100000, 999999))

            CodigoRecuperacion.objects.create(
                correo=correo,
                codigo=codigo
            )

            send_mail(
                "Código de recuperación",
                f"Tu código de recuperación es: {codigo}",
                settings.EMAIL_HOST_USER,
                [correo],
                fail_silently=False,
            )

            request.session["correo_recuperacion"] = correo

            return redirect("verificar_codigo")

    else:
        form = CorreoForm()

    return render(request, "usuarios/recuperar.html", {
        "form": form
    })


def verificar_codigo(request):
    correo = request.session.get("correo_recuperacion")

    if not correo:
        return redirect("recuperar_password")

    error = ""

    if request.method == "POST":
        form = CodigoForm(request.POST)

        if form.is_valid():
            codigo = form.cleaned_data["codigo"]

            existe = CodigoRecuperacion.objects.filter(
                correo=correo,
                codigo=codigo
            ).exists()

            if existe:
                request.session["codigo_correcto"] = True

                CodigoRecuperacion.objects.filter(
                    correo=correo,
                    codigo=codigo
                ).delete()

                return redirect("cambiar_password")
            else:
                error = "Código incorrecto."

    else:
        form = CodigoForm()

    return render(request, "usuarios/verificar_codigo.html", {
        "form": form,
        "error": error
    })


def cambiar_password(request):
    if not request.session.get("codigo_correcto"):
        return redirect("recuperar_password")

    correo = request.session.get("correo_recuperacion")

    if request.method == "POST":
        form = NuevaPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            confirmar = form.cleaned_data["confirmar"]

            if password == confirmar:
                usuario = User.objects.get(email=correo)
                usuario.set_password(password)
                usuario.save()

                CodigoRecuperacion.objects.filter(correo=correo).delete()

                request.session.flush()

                messages.success(request, "Contraseña actualizada correctamente.")

                return redirect("/accounts/login/")

    else:
        form = NuevaPasswordForm()

    return render(request, "usuarios/cambiar_password.html", {
        "form": form
    })
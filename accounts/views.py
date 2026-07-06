from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count
from django.http import HttpResponse

from .forms import RegistroForm, PerfilForm
from reporte.models import Reporte

from .forms import RegistroForm, PerfilForm
from reporte.models import Reporte
from .forms import RegistroForm, PerfilForm
from reporte.models import Reporte


def seleccion(request):
    return render(request, "accounts/seleccion.html")


def acceso(request):
    tipo = request.GET.get("tipo")
    request.session["tipo"] = tipo
    return redirect("/accounts/login/")


def registro(request):

    if request.method == "POST":

        formulario = RegistroForm(request.POST)

        if formulario.is_valid():

            usuario = User.objects.create_user(
                username=formulario.cleaned_data["username"],
                email=formulario.cleaned_data["email"],
                password=formulario.cleaned_data["password"]
            )

            usuario.save()

            return redirect("login")

    else:

        formulario = RegistroForm()

    return render(request, "registration/registro.html", {
        "formulario": formulario
    })


@login_required
def validar_acceso(request):

    tipo = request.session.get("tipo")

    # Si no seleccionó tipo de acceso
    if not tipo:
        logout(request)
        return redirect("/")

    # Usuario normal intentando entrar como administrador
    if tipo == "admin" and not request.user.is_superuser:

        logout(request)

        return render(request, "accounts/error_admin.html")

    # Administrador intentando entrar como usuario
    if tipo == "usuario" and request.user.is_superuser:

        logout(request)

        return render(request, "accounts/error_usuario.html")

    return redirect("/reporte/")

@login_required
def lista_usuarios(request):

    if not request.user.is_superuser:
        return redirect("/reporte/")

    usuarios = User.objects.annotate(
        total_reportes=Count("reporte")
    )

    return render(request, "accounts/lista_usuarios.html", {
        "usuarios": usuarios
    })
@login_required
def cambiar_estado_usuario(request, id):

    if not request.user.is_superuser:
        return redirect("/reporte/")

    usuario = User.objects.get(id=id)

    if usuario != request.user:
        usuario.is_active = not usuario.is_active
        usuario.save()

    return redirect("lista_usuarios")


@login_required
def cambiar_admin_usuario(request, id):

    if not request.user.is_superuser:
        return redirect("/reporte/")

    usuario = User.objects.get(id=id)

    if usuario != request.user:
        usuario.is_superuser = not usuario.is_superuser
        usuario.is_staff = usuario.is_superuser
        usuario.save()

    return redirect("lista_usuarios")


@login_required
def eliminar_usuario(request, id):

    if not request.user.is_superuser:
        return redirect("/reporte/")

    usuario = User.objects.get(id=id)

    if usuario != request.user:
        usuario.delete()

    return redirect("lista_usuarios")


@login_required
def reportes_usuario(request, id):

    if not request.user.is_superuser:
        return redirect("/reporte/")

    usuario = User.objects.get(id=id)

    reportes = Reporte.objects.filter(usuario=usuario)

    return render(request, "accounts/reportes_usuario.html", {
        "usuario": usuario,
        "reportes": reportes
    })


@login_required
def perfil(request):

    if request.method == "POST":

        form = PerfilForm(request.POST)

        if form.is_valid():

            request.user.username = form.cleaned_data["username"]
            request.user.email = form.cleaned_data["email"]

            request.user.save()

            return redirect("/reporte/")

    else:

        form = PerfilForm(initial={
            "username": request.user.username,
            "email": request.user.email
        })

    return render(request, "accounts/perfil.html", {
        "form": form
    })
from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class RegistroForm(forms.ModelForm):

    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su usuario"
        })
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su correo"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su contraseña"
        })
    )

    confirmar = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Repita su contraseña"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def clean(self):
        datos = super().clean()

        if datos.get("password") != datos.get("confirmar"):
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return datos


class PerfilForm(forms.Form):

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )
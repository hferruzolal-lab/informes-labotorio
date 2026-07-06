from django import forms

class CorreoForm(forms.Form):
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su correo"
        })
    )


class CodigoForm(forms.Form):
    codigo = forms.CharField(
        max_length=6,
        label="Código",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese el código"
        })
    )


class NuevaPasswordForm(forms.Form):
    password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    confirmar = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
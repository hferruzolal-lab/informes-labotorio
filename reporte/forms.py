from django import forms
from .models import Reporte


class ReporteForm(forms.ModelForm):

    class Meta:
        model = Reporte
        fields = [
            'nombre',
            'cedula',
            'laboratorio',
            'equipo',
            'descripcion',
            'estado',
            'imagen',
        ]

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        if usuario and not usuario.is_superuser:
           self.fields.pop('estado', None)
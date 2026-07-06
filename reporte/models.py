from django.db import models
from django.contrib.auth.models import User


class Reporte(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    laboratorio = models.CharField(max_length=100)
    equipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En proceso', 'En proceso'),
            ('Resuelto', 'Resuelto'),
        ],
        default='Pendiente'
    )

    imagen = models.ImageField(
        upload_to='reportes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.equipo}"


class HistorialReporte(models.Model):

    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        related_name="historial"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=255)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"
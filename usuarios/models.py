from django.db import models

class CodigoRecuperacion(models.Model):
    correo = models.EmailField()
    codigo = models.CharField(max_length=6)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.correo} - {self.codigo}"
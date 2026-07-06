from django.urls import path
from . import views

urlpatterns = [
    path("recuperar/", views.recuperar_password, name="recuperar_password"),
    path("verificar-codigo/", views.verificar_codigo, name="verificar_codigo"),
    path("cambiar-password/", views.cambiar_password, name="cambiar_password"),
]
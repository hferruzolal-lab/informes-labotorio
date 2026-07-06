from django.urls import path
from . import views

urlpatterns = [
    path('', views.seleccion, name='seleccion'),
    path('acceso/', views.acceso, name='acceso'),
    path('validar/', views.validar_acceso, name='validar'),
    path('registro/', views.registro, name='registro'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/estado/<int:id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    path('usuarios/admin/<int:id>/', views.cambiar_admin_usuario, name='cambiar_admin_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/reportes/<int:id>/', views.reportes_usuario, name='reportes_usuario'),

    path('perfil/', views.perfil, name='perfil'),
    path(
    'usuarios/reportes/<int:id>/',
    views.reportes_usuario,
    name='reportes_usuario'
    
),
path('usuarios/', views.lista_usuarios, name='lista_usuarios'),

path(
    'usuarios/reportes/<int:id>/',
    views.reportes_usuario,
    name='reportes_usuario'
),
]
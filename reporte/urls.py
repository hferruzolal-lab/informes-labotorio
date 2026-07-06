from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('editar/<int:id>/', views.editar_reporte, name='editar_reporte'),
    path('eliminar/<int:id>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('pdf/', views.reporte_pdf, name='reporte_pdf'),
    path('excel/', views.reporte_excel, name='reporte_excel'),
    path('historial/<int:id>/', views.historial_reporte, name='historial_reporte'),

    # NUEVO
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]
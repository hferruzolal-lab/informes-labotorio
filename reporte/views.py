from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import Reporte, HistorialReporte
from .forms import ReporteForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.functions import TruncMonth
import json


@login_required
def inicio(request):

    print(request.user.username, request.user.is_superuser, request.user.is_staff)

    buscar = request.GET.get('buscar', '')

    if request.user.is_superuser:
        reportes = Reporte.objects.all()
    else:
        reportes = Reporte.objects.filter(usuario=request.user)

    if buscar:
        reportes = reportes.filter(
            Q(nombre__icontains=buscar) |
            Q(equipo__icontains=buscar) |
            Q(laboratorio__icontains=buscar)
        )

    total = Reporte.objects.count()
    pendientes = Reporte.objects.filter(estado="Pendiente").count()
    proceso = Reporte.objects.filter(estado="En proceso").count()
    resueltos = Reporte.objects.filter(estado="Resuelto").count()

    return render(request, 'inicio.html', {
        'reportes': reportes,
        'buscar': buscar,
        'total': total,
        'pendientes': pendientes,
        'proceso': proceso,
        'resueltos': resueltos,
    })


@login_required
def nuevo_reporte(request):

    if request.method == 'POST':

        formulario = ReporteForm(
            request.POST,
            request.FILES,
            usuario=request.user
        )

        if formulario.is_valid():

            reporte = formulario.save(commit=False)
            reporte.usuario = request.user
            reporte.save()

            HistorialReporte.objects.create(
                reporte=reporte,
                usuario=request.user,
                accion="Creó el reporte"
            )

            return redirect('inicio')

    else:

        formulario = ReporteForm(usuario=request.user)

    return render(request, 'nuevo_reporte.html', {
        'formulario': formulario
    })


@login_required
def editar_reporte(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para editar reportes.")

    reporte = get_object_or_404(Reporte, id=id)

    estado_anterior = reporte.estado

    if request.method == "POST":

        formulario = ReporteForm(
            request.POST,
            request.FILES,
            instance=reporte,
            usuario=request.user
        )

        if formulario.is_valid():

            reporte_editado = formulario.save()

            if estado_anterior != reporte_editado.estado:

                HistorialReporte.objects.create(
                    reporte=reporte_editado,
                    usuario=request.user,
                    accion=f"Cambió el estado a {reporte_editado.estado}"
                )

                if reporte_editado.usuario and reporte_editado.usuario.email:

                    send_mail(
                        "Actualización de reporte",
                        f"Hola {reporte_editado.usuario.username},\n\n"
                        f"El estado de tu reporte ha sido actualizado.\n\n"
                        f"Equipo: {reporte_editado.equipo}\n"
                        f"Laboratorio: {reporte_editado.laboratorio}\n"
                        f"Nuevo estado: {reporte_editado.estado}\n\n"
                        f"Gracias por utilizar Nuestro Reporte de Daños.",
                        settings.EMAIL_HOST_USER,
                        [reporte_editado.usuario.email],
                        fail_silently=False,
                    )

            return redirect("inicio")

    else:

        formulario = ReporteForm(
            instance=reporte,
            usuario=request.user
        )

    return render(request, "nuevo_reporte.html", {
        "formulario": formulario
    })


@login_required
def eliminar_reporte(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para eliminar reportes.")

    reporte = get_object_or_404(Reporte, id=id)

    HistorialReporte.objects.create(
        reporte=reporte,
        usuario=request.user,
        accion="Eliminó el reporte"
    )

    reporte.delete()

    return redirect("inicio")


@login_required
def reporte_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reportes.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Reporte de Daños")

    p.setFont("Helvetica", 11)

    y = 760

    if request.user.is_superuser:
        reportes = Reporte.objects.all()
    else:
        reportes = Reporte.objects.filter(usuario=request.user)

    for reporte in reportes:

        texto = (
            f"Nombre: {reporte.nombre} | "
            f"Equipo: {reporte.equipo} | "
            f"Laboratorio: {reporte.laboratorio} | "
            f"Estado: {reporte.estado}"
        )

        p.drawString(40, y, texto)

        y -= 20

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 11)
            y = 800

    p.save()

    return response


@login_required
def reporte_excel(request):
    wb = Workbook()

    ws = wb.active
    ws.title = "Reportes"

    ws.append([
        "Nombre",
        "Cédula",
        "Fecha",
        "Laboratorio",
        "Equipo",
        "Estado"
    ])

    if request.user.is_superuser:
        reportes = Reporte.objects.all()
    else:
        reportes = Reporte.objects.filter(usuario=request.user)

    for reporte in reportes:

        ws.append([
            reporte.nombre,
            reporte.cedula,
            reporte.fecha.strftime("%d/%m/%Y %H:%M"),
            reporte.laboratorio,
            reporte.equipo,
            reporte.estado
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="reportes.xlsx"'

    wb.save(response)

    return response
@login_required
def historial_reporte(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "No tienes permiso para ver el historial."
        )

    reporte = get_object_or_404(Reporte, id=id)

    historial = HistorialReporte.objects.filter(
        reporte=reporte
    ).order_by("-fecha")

    return render(
        request,
        "historial_reporte.html",
        {
            "reporte": reporte,
            "historial": historial
        }
    )
@login_required
def estadisticas(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden(
            "No tienes permiso para ver las estadísticas."
        )

    # Reportes por laboratorio
    reportes_laboratorio = Reporte.objects.values(
        "laboratorio"
    ).annotate(
        total=Count("id")
    ).order_by("-total")

    laboratorios_labels = []
    laboratorios_data = []

    for item in reportes_laboratorio:
        laboratorios_labels.append(item["laboratorio"])
        laboratorios_data.append(item["total"])

    # Reportes por mes
    reportes_mes = Reporte.objects.annotate(
        mes=TruncMonth("fecha")
    ).values(
        "mes"
    ).annotate(
        total=Count("id")
    ).order_by("mes")

    meses_labels = []
    meses_data = []

    for item in reportes_mes:
        meses_labels.append(item["mes"].strftime("%m/%Y"))
        meses_data.append(item["total"])

    # Reportes por usuario
    reportes_usuario = Reporte.objects.values(
        "usuario__username"
    ).annotate(
        total=Count("id")
    ).order_by("-total")

    usuarios_labels = []
    usuarios_data = []

    for item in reportes_usuario:
        if item["usuario__username"]:
            usuarios_labels.append(item["usuario__username"])
        else:
            usuarios_labels.append("Sin usuario")

        usuarios_data.append(item["total"])

    # Reportes por estado
    pendientes = Reporte.objects.filter(estado="Pendiente").count()
    proceso = Reporte.objects.filter(estado="En proceso").count()
    resueltos = Reporte.objects.filter(estado="Resuelto").count()

    return render(request, "estadisticas.html", {
        "laboratorios_labels": json.dumps(laboratorios_labels),
        "laboratorios_data": json.dumps(laboratorios_data),

        "meses_labels": json.dumps(meses_labels),
        "meses_data": json.dumps(meses_data),

        "usuarios_labels": json.dumps(usuarios_labels),
        "usuarios_data": json.dumps(usuarios_data),

        "estados_labels": json.dumps([
            "Pendiente",
            "En proceso",
            "Resuelto"
        ]),
        "estados_data": json.dumps([
            pendientes,
            proceso,
            resueltos
        ]),

        "pendientes": pendientes,
        "proceso": proceso,
        "resueltos": resueltos,
    })
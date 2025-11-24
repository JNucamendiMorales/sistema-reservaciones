# chart_views.py
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
from myapp.models import Salon, Reservacion


# === Charts: Reservaciones ===
def obtener_datos_reservaciones(request):
    hoy = timezone.now().date()
    periodo = request.GET.get("periodo", "semana")
    modo = request.GET.get("modo", "mejores")

    if periodo == "mes":
        inicio_mes = hoy.replace(day=1)
        fin_mes = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        fecha_inicio, fecha_fin = inicio_mes, fin_mes
    else:
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        fecha_inicio, fecha_fin = inicio_semana, fin_semana

    reservaciones = Reservacion.objects.filter(fecha_reserva__range=[fecha_inicio, fecha_fin])

    # Por día
    if periodo == "semana":
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        base_dias = {d: 0 for d in dias_semana}
        for item in reservaciones.values("fecha_reserva").annotate(total=Count("id")):
            dia = dias_semana[item["fecha_reserva"].weekday()]
            base_dias[dia] += item["total"]
        por_dia = [{"fecha_reserva": k, "total": v} for k, v in base_dias.items()]
    else:
        total_dias = calendar.monthrange(hoy.year, hoy.month)[1]
        rangos = {}
        for start in range(1, total_dias + 1, 5):
            end = min(start + 4, total_dias)
            etiqueta = f"{start}-{end}"
            rangos[etiqueta] = 0
        for item in reservaciones.values("fecha_reserva").annotate(total=Count("id")):
            dia = item["fecha_reserva"].day
            rango_inicio = ((dia - 1) // 5) * 5 + 1
            rango_fin = min(rango_inicio + 4, total_dias)
            etiqueta = f"{rango_inicio}-{rango_fin}"
            rangos[etiqueta] += item["total"]
        por_dia = [{"fecha_reserva": k, "total": v} for k, v in rangos.items()]

    # Ingresos por día
    if periodo == "semana":
        base_dias_ingresos = {d: 0 for d in dias_semana}
        for item in reservaciones.values("fecha_reserva").annotate(total=Sum("precio_total")):
            dia = dias_semana[item["fecha_reserva"].weekday()]
            base_dias_ingresos[dia] += item["total"]
        ingresos_por_dia = [{"fecha_reserva": k, "total": v} for k, v in base_dias_ingresos.items()]
    else:
        rangos_ingresos = {k: 0 for k in rangos.keys()}
        for item in reservaciones.values("fecha_reserva").annotate(total=Sum("precio_total")):
            dia = item["fecha_reserva"].day
            rango_inicio = ((dia - 1) // 5) * 5 + 1
            rango_fin = min(rango_inicio + 4, total_dias)
            etiqueta = f"{rango_inicio}-{rango_fin}"
            rangos_ingresos[etiqueta] += item["total"]
        ingresos_por_dia = [{"fecha_reserva": k, "total": v} for k, v in rangos_ingresos.items()]

    # Por salón
    por_salon = list(
        reservaciones.values("salon__nombre").annotate(total=Count("id")).order_by("-total")
    )

    # Por estado
    por_estado = list(
        reservaciones.values("estado").annotate(total=Count("id")).order_by("-total")
    )

    # Modo peores
    if modo == "peores":
        por_dia.reverse()
        por_estado.reverse()
        ingresos_por_dia.reverse()

    data = {
        "por_dia": por_dia,
        "por_salon": por_salon,
        "por_estado": por_estado,
        "ingresos_por_dia": ingresos_por_dia,
        "periodo": periodo,
        "modo": modo,
        "rango": f"{fecha_inicio} → {fecha_fin}",
    }
    return JsonResponse(data)


# === Charts: Usuarios ===
def obtener_datos_usuarios(request):
    hoy = timezone.localtime().date()
    periodo = request.GET.get("periodo", "semana")
    modo = request.GET.get("modo", "mejores")

    if periodo == "mes":
        inicio = hoy.replace(day=1)
        fin = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
    else:
        inicio = hoy - timedelta(days=hoy.weekday())
        fin = inicio + timedelta(days=6)

    inicio_aware = make_aware(datetime.combine(inicio, datetime.min.time()))
    fin_aware = make_aware(datetime.combine(fin, datetime.max.time()))

    usuarios_rango = User.objects.filter(date_joined__range=[inicio_aware, fin_aware])

    # Nuevos usuarios
    if periodo == "semana":
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        conteo = {dia: 0 for dia in dias_semana}
        for u in usuarios_rango:
            dia = u.date_joined.weekday()
            conteo[dias_semana[dia]] += 1
        nuevos_usuarios = [{"fecha": d, "total": t} for d, t in conteo.items()]
    else:
        total_dias = calendar.monthrange(hoy.year, hoy.month)[1]
        rangos = {}
        for start in range(1, total_dias+1, 5):
            end = min(start+4, total_dias)
            etiqueta = f"{start}-{end}"
            rangos[etiqueta] = 0
        for u in usuarios_rango:
            dia = u.date_joined.day
            for r in rangos.keys():
                start, end = map(int, r.split('-'))
                if start <= dia <= end:
                    rangos[r] += 1
                    break
        nuevos_usuarios = [{"fecha": k, "total": v} for k, v in rangos.items()]

    # Usuarios con mayores ingresos
    reservaciones_rango = Reservacion.objects.filter(fecha_reserva__range=[inicio, fin])
    ingresos_por_usuario = (
        reservaciones_rango.values("usuario__username")
        .annotate(total=Sum("precio_total"))
        .order_by("-total")
    )
    usuarios_ingresos = [
        {"usuario": u["usuario__username"], "total": float(u["total"] or 0)}
        for u in ingresos_por_usuario
    ]
    if not usuarios_ingresos:
        usuarios_ingresos = [{"usuario": u.username, "total": 0.0} for u in User.objects.all()[:5]]

    # Usuarios más activos
    usuarios_activos_qs = (
        reservaciones_rango.values("usuario__username")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    usuarios_activos = [{"usuario": u["usuario__username"], "total": u["total"]} for u in usuarios_activos_qs]
    if not usuarios_activos:
        usuarios_activos = [{"usuario": u.username, "total": 0} for u in User.objects.all()[:5]]

    # Modo peores
    if modo == "peores":
        nuevos_usuarios.reverse()
        usuarios_ingresos.reverse()
        usuarios_activos.reverse()

    data = {
        "nuevos_usuarios": nuevos_usuarios,
        "usuarios_ingresos": usuarios_ingresos[:5],
        "usuarios_activos": usuarios_activos[:5],
        "periodo": periodo,
        "modo": modo,
        "rango": f"{inicio} → {fin}",
    }
    return JsonResponse(data)


# === Charts: Salones ===
def obtener_datos_salones(request):
    total_salones = Salon.objects.count()
    disponibles = Salon.objects.filter(disponible=True).count()
    ocupados = Salon.objects.filter(disponible=False).count()
    categorias = Salon.objects.values('categoria').annotate(total=models.Count('id'))

    data = {
        "totales": {
            "total_salones": total_salones,
            "disponibles": disponibles,
            "ocupados": ocupados,
        },
        "categorias": list(categorias)
    }
    return JsonResponse(data)


# === Vistas render HTML ===
def chart_reservaciones(request):
    return render(request, 'admin_custom/chart_reservaciones.html')


def chart_usuarios(request):
    return render(request, 'admin_custom/chart_usuarios.html')


def chart_salones(request):
    salones = list(Salon.objects.all().values())
    return render(request, "admin_custom/chart_salones.html", {"salones": salones})

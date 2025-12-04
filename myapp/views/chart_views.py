# chart_views.py
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
from myapp.models import Salon, Reservacion


# === Charts: Reservaciones ===
def obtener_datos_reservaciones(request):
    periodo = request.GET.get("periodo", "semana")

    # BAR CHART: por_dia debe ser el conteo de reservaciones (Count)
    # LINE CHART: ingresos_por_dia debe ser la suma de precio_total (Sum)
    if periodo == "semana":
        hoy = now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Conteos por día (Count)
        qs_counts = (
            Reservacion.objects
            .filter(fecha_reserva__range=[inicio_semana, inicio_semana + timedelta(days=6)])
            .values("fecha_reserva")
            .annotate(total=Count("id"))
            .order_by("fecha_reserva")
        )
        counts_map = {r["fecha_reserva"].isoformat(): int(r["total"] or 0) for r in qs_counts}

        # Ingresos por día (Sum)
        qs_sums = (
            Reservacion.objects
            .filter(fecha_reserva__range=[inicio_semana, inicio_semana + timedelta(days=6)])
            .values("fecha_reserva")
            .annotate(total=Sum("precio_total"))
            .order_by("fecha_reserva")
        )
        sums_map = {r["fecha_reserva"].isoformat(): float(r["total"] or 0.0) for r in qs_sums}

        por_dia = []
        ingresos_por_dia = []
        for i in range(7):
            dia = inicio_semana + timedelta(days=i)
            iso = dia.isoformat()
            por_dia.append({"fecha_reserva": dias_nombres[i], "total": counts_map.get(iso, 0)})
            ingresos_por_dia.append({"fecha_reserva": dias_nombres[i], "total": sums_map.get(iso, 0.0)})

    elif periodo == "mes":
        rangos = [(1,5), (6,10), (11,15), (16,20), (21,25), (26,31)]
        mes_actual = now().month
        año_actual = now().year

        por_dia = []
        ingresos_por_dia = []
        for inicio_d, fin_d in rangos:
            qs_range = Reservacion.objects.filter(
                fecha_reserva__year=año_actual,
                fecha_reserva__month=mes_actual,
                fecha_reserva__day__gte=inicio_d,
                fecha_reserva__day__lte=fin_d
            )
            total_count = qs_range.aggregate(total=Count("id"))["total"] or 0
            total_sum = qs_range.aggregate(total=Sum("precio_total"))["total"] or 0.0
            label = f"{inicio_d}-{fin_d}"
            por_dia.append({"fecha_reserva": label, "total": int(total_count)})
            ingresos_por_dia.append({"fecha_reserva": label, "total": float(total_sum)})

    # Salones más reservados (sigue igual, counts)
    por_salon = Reservacion.objects.values("salon__nombre").annotate(total=Count("id")).order_by("-total")[:10]

    return JsonResponse({
        "por_dia": por_dia,                 # para el gráfico de barras (conteos)
        "por_salon": list(por_salon),
        "ingresos_por_dia": ingresos_por_dia,  # para el gráfico de ingresos (montos)
    })


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

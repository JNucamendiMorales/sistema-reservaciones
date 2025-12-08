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


# ---------------------------
# Helper: calcular rango local (CDMX) para periodo
# ---------------------------
def _local_period_range(period, reference_dt=None):
    """
    Devuelve (start_date, end_date, start_aware, end_aware) en zona horaria local.
    - 'semana': semana desde Lunes hasta Domingo (se reinicia al Lunes 00:00)
    - 'mes'  : mes completo (1..ultimo_dia) (se reinicia al primer día del mes 00:00)
    """
    ref = reference_dt or timezone.localtime()
    # asegurarnos de usar la hora local configurada en settings
    local_now = timezone.localtime(ref)
    if period == "mes":
        start_date = local_now.replace(day=1).date()
        last_day = calendar.monthrange(local_now.year, local_now.month)[1]
        end_date = local_now.replace(day=last_day).date()
    else:
        # semana: lunes .. domingo (reinicia el Lunes 00:00)
        start_date = (local_now - timedelta(days=local_now.weekday())).date()
        end_date = start_date + timedelta(days=6)

    start_aware = make_aware(datetime.combine(start_date, datetime.min.time()))
    end_aware = make_aware(datetime.combine(end_date, datetime.max.time()))
    return start_date, end_date, start_aware, end_aware


# === Charts: Reservaciones ===
def obtener_datos_reservaciones(request):
    periodo = request.GET.get("periodo", "semana")

    # BAR CHART: por_dia debe ser el conteo de reservaciones (Count)
    # LINE CHART: ingresos_por_dia debe ser la suma de precio_total (Sum)
    if periodo == "semana":
        # usar helper local para asegurar que la semana corresponde a Lunes..Domingo
        inicio_semana_date, fin_semana_date, _, _ = _local_period_range("semana")
        dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Conteos por día (Count)
        qs_counts = (
            Reservacion.objects
            .filter(fecha_reserva__range=[inicio_semana_date, fin_semana_date])
            .values("fecha_reserva")
            .annotate(total=Count("id"))
            .order_by("fecha_reserva")
        )
        counts_map = {r["fecha_reserva"].isoformat(): int(r["total"] or 0) for r in qs_counts}

        # Ingresos por día (Sum)
        qs_sums = (
            Reservacion.objects
            .filter(fecha_reserva__range=[inicio_semana_date, fin_semana_date])
            .values("fecha_reserva")
            .annotate(total=Sum("precio_total"))
            .order_by("fecha_reserva")
        )
        sums_map = {r["fecha_reserva"].isoformat(): float(r["total"] or 0.0) for r in qs_sums}

        por_dia = []
        ingresos_por_dia = []
        for i in range(7):
            dia = inicio_semana_date + timedelta(days=i)
            iso = dia.isoformat()
            por_dia.append({"fecha_reserva": dias_nombres[i], "total": counts_map.get(iso, 0)})
            ingresos_por_dia.append({"fecha_reserva": dias_nombres[i], "total": sums_map.get(iso, 0.0)})

    elif periodo == "mes":
        # usar helper local para mes completo
        inicio_mes_date, fin_mes_date, _, _ = _local_period_range("mes")
        rangos = [(1,5), (6,10), (11,15), (16,20), (21,25), (26,31)]
        mes_actual = inicio_mes_date.month
        año_actual = inicio_mes_date.year

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
    # usar la hora local para cálculo consistente
    periodo = request.GET.get("periodo", "semana")
    modo = request.GET.get("modo", "mejores")

    inicio_date, fin_date, inicio_aware, fin_aware = _local_period_range(periodo)

    usuarios_rango = User.objects.filter(date_joined__range=[inicio_aware, fin_aware])

    # Nuevos usuarios
    if periodo == "semana":
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        conteo = {dia: 0 for dia in dias_semana}
        for u in usuarios_rango:
            dia = timezone.localtime(u.date_joined).weekday()
            conteo[dias_semana[dia]] += 1
        nuevos_usuarios = [{"fecha": d, "total": t} for d, t in conteo.items()]
    else:
        total_dias = calendar.monthrange(inicio_date.year, inicio_date.month)[1]
        rangos = {}
        for start in range(1, total_dias+1, 5):
            end = min(start+4, total_dias)
            etiqueta = f"{start}-{end}"
            rangos[etiqueta] = 0
        for u in usuarios_rango:
            dia = timezone.localtime(u.date_joined).day
            for r in rangos.keys():
                start, end = map(int, r.split('-'))
                if start <= dia <= end:
                    rangos[r] += 1
                    break
        nuevos_usuarios = [{"fecha": k, "total": v} for k, v in rangos.items()]

    # Usuarios con mayores ingresos
    reservaciones_rango = Reservacion.objects.filter(fecha_reserva__range=[inicio_date, fin_date])
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
        "rango": f"{inicio_date} → {fin_date}",
    }
    return JsonResponse(data)


# === Charts: Salones ===
def obtener_datos_salones(request):
    """Obtiene datos de salones con ingresos por período"""
    from django.db.models import Sum, Avg
    import calendar
    import pytz
    from datetime import datetime, timedelta
    
    periodo = request.GET.get("periodo", "semana")
    inicio_date, fin_date, inicio_aware, fin_aware = _local_period_range(periodo)

    # ===== TOP 5 CALIFICACIÓN (del campo calificacion del Salon) =====
    top_calificacion = list(
        Salon.objects
        .values("nombre", "calificacion")
        .order_by("-calificacion")[:5]
    )

    # ===== TOP 5 PRECIOS =====
    top_precios = list(
        Salon.objects
        .values("nombre", "precio")
        .order_by("-precio")[:5]
    )

    # ===== TOP 5 INGRESOS POR PERÍODO =====
    if periodo == "semana":
        dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        tz = pytz.timezone('America/Mexico_City')
        
        salones_ingresos = {}
        for i in range(7):
            d = inicio_date + timedelta(days=i)
            start_dt = datetime.combine(d, datetime.min.time())
            end_dt = datetime.combine(d, datetime.max.time())
            if start_dt.tzinfo is None:
                start_dt = tz.localize(start_dt)
            if end_dt.tzinfo is None:
                end_dt = tz.localize(end_dt)
            
            qs = Reservacion.objects.filter(
                fecha_reserva__range=[start_dt, end_dt]
            ).values("salon__nombre").annotate(total=Sum("precio_total"))
            
            for item in qs:
                salon_name = item["salon__nombre"]
                if salon_name not in salones_ingresos:
                    salones_ingresos[salon_name] = [0.0] * 7
                salones_ingresos[salon_name][i] = float(item["total"] or 0.0)
        
        totales_salon = {k: sum(v) for k, v in salones_ingresos.items()}
        top_salones = sorted(totales_salon.items(), key=lambda x: x[1], reverse=True)[:5]
        
        ingresos_data = []
        for salon_name, _ in top_salones:
            ingresos_data.append({
                "salon": salon_name,
                "labels": dias_nombres,
                "data": salones_ingresos.get(salon_name, [0.0] * 7)
            })

    else:  # mes
        rangos = [(1, 5, "1-5"), (6, 10, "6-10"), (11, 15, "11-15"), (16, 20, "16-20"), (21, 25, "21-25"), (26, 31, "26-31")]
        
        salones_ingresos = {}
        for start, end, label in rangos:
            qs = Reservacion.objects.filter(
                fecha_reserva__year=inicio_date.year,
                fecha_reserva__month=inicio_date.month,
                fecha_reserva__day__gte=start,
                fecha_reserva__day__lte=end
            ).values("salon__nombre").annotate(total=Sum("precio_total"))
            
            for item in qs:
                salon_name = item["salon__nombre"]
                if salon_name not in salones_ingresos:
                    salones_ingresos[salon_name] = {}
                salones_ingresos[salon_name][label] = float(item["total"] or 0.0)
        
        for salon_name in salones_ingresos:
            for start, end, label in rangos:
                if label not in salones_ingresos[salon_name]:
                    salones_ingresos[salon_name][label] = 0.0
        
        totales_salon = {k: sum(v.values()) for k, v in salones_ingresos.items()}
        top_salones = sorted(totales_salon.items(), key=lambda x: x[1], reverse=True)[:5]
        
        labels_rangos = [r[2] for r in rangos]
        ingresos_data = []
        for salon_name, _ in top_salones:
            ingresos_data.append({
                "salon": salon_name,
                "labels": labels_rangos,
                "data": [salones_ingresos.get(salon_name, {}).get(label, 0.0) for label in labels_rangos]
            })

    return JsonResponse({
        "top_calificacion": top_calificacion,
        "top_precios": top_precios,
        "top_ingresos": ingresos_data,
        "periodo": periodo
    })


# === Vistas render HTML ===
def chart_reservaciones(request):
    return render(request, 'admin_custom/chart_reservaciones.html')


def chart_usuarios(request):
    return render(request, 'admin_custom/chart_usuarios.html')


def chart_salones(request):
    salones = list(Salon.objects.all().values())
    return render(request, "admin_custom/chart_salones.html", {"salones": salones})

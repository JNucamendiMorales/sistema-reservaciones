import csv
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from myapp.models import Salon, Reservacion
from myapp.Descargas.export_charts import (
    exportar_csv, 
    exportar_pdf, 
    exportar_xlsx_nativo,
    exportar_xlsx_reservaciones_semanal,
    exportar_xlsx_reservaciones_mensual,
    exportar_csv_reservaciones_semanal,
    exportar_csv_reservaciones_mensual
)


def dashboard_export(request):
    """Download CSV of all reservations"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dashboard_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Salón', 'Fecha', 'Estado', 'Precio Total'])

    reservaciones = Reservacion.objects.all().select_related('usuario', 'salon')
    for r in reservaciones:
        writer.writerow([
            r.usuario.username,
            r.salon.nombre,
            r.fecha_reserva,
            r.estado,
            r.precio_total,
        ])

    return response


def descargar_reportes(request, formato):
    periodo = request.GET.get("periodo", "semana")
    fecha_descarga = timezone.now().strftime("%d/%m/%Y %H:%M:%S")

    # Exportar CSV con datos reales según periodo
    if formato == "csv":
        if periodo == "semana":
            return exportar_csv_reservaciones_semanal(fecha_descarga)
        elif periodo == "mes":
            return exportar_csv_reservaciones_mensual(fecha_descarga)

    # Exportar XLSX con datos reales según periodo
    if formato == "xlsx":
        if periodo == "semana":
            return exportar_xlsx_reservaciones_semanal(fecha_descarga)
        elif periodo == "mes":
            return exportar_xlsx_reservaciones_mensual(fecha_descarga)

    # Para PDF usar datos genéricos (el resto del código...)
    charts_data = [
        {
            "nombre": "Reservaciones Mensuales",
            "datos": [
                {"Etiqueta": "Enero", "Valor": 45},
                {"Etiqueta": "Febrero", "Valor": 60},
                {"Etiqueta": "Marzo", "Valor": 50},
            ],
        },
        {
            "nombre": "Uso de Salones",
            "datos": [
                {"Etiqueta": "Salón A", "Valor": 80},
                {"Etiqueta": "Salón B", "Valor": 55},
                {"Etiqueta": "Salón C", "Valor": 90},
            ],
        },
        {
            "nombre": "Usuarios Activos",
            "datos": [
                {"Etiqueta": "Admin", "Valor": 3},
                {"Etiqueta": "Clientes", "Valor": 25},
                {"Etiqueta": "Invitados", "Valor": 12},
            ],
        },
    ]

    if formato == "csv":
        return exportar_csv(charts_data, fecha_descarga)

    elif formato == "pdf":
        # Solo POST permitido
        if request.method != "POST":
            return HttpResponse("Use POST para generar PDF con imágenes.", status=405)

        import json
        import base64

        # debug
        print("descargar_pdf - request.POST keys:", list(request.POST.keys()))
        print("descargar_pdf - request.FILES keys:", list(request.FILES.keys()))

        images = {}

        # 1) Intentar leer JSON body (útil cuando frontend envía application/json)
        try:
            if request.body:
                parsed = json.loads(request.body.decode("utf-8"))
                if isinstance(parsed, dict):
                    raw_imgs = parsed.get("images", parsed)
                    if isinstance(raw_imgs, dict):
                        for k, v in raw_imgs.items():
                            if v:
                                images[k] = v
        except Exception:
            pass

        # 2) Leer campo 'images' en form-data si existe (string JSON)
        if not images and request.POST.get("images"):
            try:
                parsed = json.loads(request.POST.get("images"))
                if isinstance(parsed, dict):
                    for k, v in parsed.items():
                        if v:
                            images[k] = v
            except Exception:
                pass

        # 3) Leer campos individuales en form-data
        for k in list(request.POST.keys()):
            if k == "images":
                continue
            v = request.POST.get(k)
            if v:
                images[k] = v

        # 4) Convertir archivos a base64
        for k, f in request.FILES.items():
            try:
                raw = f.read()
                images[k] = base64.b64encode(raw).decode("ascii")
            except Exception:
                pass

        # Mapear aliases
        key_map = {
            "bar": "reservaciones",
            "pie": "salones_mas_reservados",
            "line": "ingresos",
            "reservaciones_por_periodo": "reservaciones",
            "uso_de_salones": "salones_mas_reservados",
            "usuarios_activos": "ingresos",
            "reservaciones": "reservaciones",
            "salones_mas_reservados": "salones_mas_reservados",
            "ingresos": "ingresos",
        }

        normalized = {}
        for k, v in images.items():
            target = key_map.get(k, k)
            if v:
                normalized[target] = v

        images = {k: v for k, v in normalized.items() if v}
        print("descargar_pdf - images keys after mapping:", list(images.keys()))

        required = ["reservaciones", "salones_mas_reservados", "ingresos"]
        missing = [r for r in required if r not in images]
        if missing:
            return HttpResponse(
                f"Faltan imágenes para: {', '.join(missing)}.",
                status=400,
            )

        # Obtener periodo del query string O del POST
        periodo = request.POST.get("periodo") or request.GET.get("periodo", "semana")
        
        # --- Generar charts_data según periodo ---
        now_dt = timezone.now().date()
        
        if periodo == "semana":
            inicio = now_dt - timedelta(days=now_dt.weekday())
            dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            datos_periodo = []
            for i in range(7):
                d = inicio + timedelta(days=i)
                total = Reservacion.objects.filter(fecha_reserva=d).count()
                datos_periodo.append({"Etiqueta": dias_nombres[i], "Valor": total})
        else:  # mes
            mes_actual = now_dt.month
            año_actual = now_dt.year
            rangos = [(1, 5, "1-5"), (6, 10, "6-10"), (11, 15, "11-15"), (16, 20, "16-20"), (21, 25, "21-25"), (26, 31, "26-31")]
            datos_periodo = []
            for start, end, label in rangos:
                total = Reservacion.objects.filter(
                    fecha_reserva__year=año_actual,
                    fecha_reserva__month=mes_actual,
                    fecha_reserva__day__gte=start,
                    fecha_reserva__day__lte=end,
                ).count()
                datos_periodo.append({"Etiqueta": label, "Valor": total})

        # Uso de salones (top 10) - igual en ambos periodos
        por_salon_qs = Reservacion.objects.values("salon__nombre").annotate(total=Count("id")).order_by("-total")[:10]
        datos_salones = [{"Etiqueta": s["salon__nombre"], "Valor": s["total"]} for s in por_salon_qs]

        # Ingresos por periodo
        if periodo == "semana":
            inicio_dt = inicio
            fin_dt = now_dt
            ingresos_list = []
            dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            for i in range(7):
                d = inicio + timedelta(days=i)
                total_ingreso = (Reservacion.objects
                                 .filter(fecha_reserva=d)
                                 .aggregate(total=Sum("precio_total"))["total"] or 0.0)
                ingresos_list.append({"Etiqueta": dias_nombres[i], "Valor": float(total_ingreso)})
        else:  # mes
            rangos = [(1, 5, "1-5"), (6, 10, "6-10"), (11, 15, "11-15"), (16, 20, "16-20"), (21, 25, "21-25"), (26, 31, "26-31")]
            ingresos_list = []
            for start, end, label in rangos:
                total_ingreso = (Reservacion.objects
                                 .filter(
                                     fecha_reserva__year=now_dt.year,
                                     fecha_reserva__month=now_dt.month,
                                     fecha_reserva__day__gte=start,
                                     fecha_reserva__day__lte=end
                                 )
                                 .aggregate(total=Sum("precio_total"))["total"] or 0.0)
                ingresos_list.append({"Etiqueta": label, "Valor": float(total_ingreso)})

        charts_data_real = [
            {"nombre": "Reservaciones por periodo", "datos": datos_periodo},
            {"nombre": "Uso de Salones", "datos": datos_salones},
            {"nombre": "Ingresos por periodo", "datos": ingresos_list},
        ]

        # Determinar título según periodo
        titulo_reporte = "Reporte Semanal de Reservaciones" if periodo == "semana" else "Reporte Mensual de Reservaciones"

        try:
            return exportar_pdf(charts_data_real, images, fecha_descarga=fecha_descarga, titulo_reporte=titulo_reporte)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        except Exception as e:
            import traceback; traceback.print_exc()
            return HttpResponse("Error al generar PDF", status=500)

    else:
        return HttpResponse("Formato no válido", status=400)
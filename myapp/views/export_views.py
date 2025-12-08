import csv
import json
import base64
import traceback
import pytz
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # AGREGAR ESTO
from myapp.models import Salon, Reservacion
from myapp.Descargas.export_csv import (
    exportar_csv,
    exportar_csv_reservaciones_semanal,
    exportar_csv_reservaciones_mensual,
    exportar_csv_usuarios_semanal,
    exportar_csv_usuarios_mensual,
    exportar_csv_salones_semanal,       # NEW
    exportar_csv_salones_mensual        # NEW
)
from myapp.Descargas.export_pdf import exportar_pdf, exportar_pdf_usuarios_semanal, exportar_pdf_usuarios_mensual

# reemplazar importaciones directas problemáticas por import del módulo y mapeo seguro

# OLD imports (elimínalos o coméntalos)
# from myapp.Descargas.export_xlsx import (
#     exportar_xlsx_usuarios_semanal,
#     exportar_xlsx_usuarios_mensual,
#     exportar_xlsx_reservaciones_semanal,
#     exportar_xlsx_reservaciones_mensual,
#     exportar_xlsx_salones_semanal,
#     exportar_xlsx_salones_mensual
# )

# NEW: importar el módulo y mapear funciones si existen
import importlib
export_xlsx = importlib.import_module("myapp.Descargas.export_xlsx")

exportar_xlsx_usuarios_semanal = getattr(export_xlsx, "exportar_xlsx_usuarios_semanal", None)
exportar_xlsx_usuarios_mensual = getattr(export_xlsx, "exportar_xlsx_usuarios_mensual", None)
exportar_xlsx_reservaciones_semanal = getattr(export_xlsx, "exportar_xlsx_reservaciones_semanal", None)
exportar_xlsx_reservaciones_mensual = getattr(export_xlsx, "exportar_xlsx_reservaciones_mensual", None)
exportar_xlsx_salones_semanal = getattr(export_xlsx, "exportar_xlsx_salones_semanal", None)
exportar_xlsx_salones_mensual = getattr(export_xlsx, "exportar_xlsx_salones_mensual", None)


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


@login_required
def descargar_reportes(request, formato):
    periodo = request.GET.get("periodo", "semana")
    tipo = request.GET.get("tipo", request.POST.get("tipo", "reservaciones"))
    
    tz = pytz.timezone('America/Mexico_City')
    now_local = timezone.now().astimezone(tz)
    fecha_descarga = now_local.strftime("%d/%m/%Y %H:%M:%S")

    # === CSV ===
    if formato == "csv":
        if tipo == "usuarios":
            return exportar_csv_usuarios_semanal(fecha_descarga) if periodo == "semana" else exportar_csv_usuarios_mensual(fecha_descarga)
        elif tipo == "salones":
            return exportar_csv_salones_semanal(fecha_descarga) if periodo == "semana" else exportar_csv_salones_mensual(fecha_descarga)
        else:
            return exportar_csv_reservaciones_semanal(fecha_descarga) if periodo == "semana" else exportar_csv_reservaciones_mensual(fecha_descarga)

    # === XLSX ===
    if formato == "xlsx":
        if tipo == "usuarios":
            return exportar_xlsx_usuarios_semanal(fecha_descarga) if periodo == "semana" else exportar_xlsx_usuarios_mensual(fecha_descarga)
        elif tipo == "salones":
            return exportar_xlsx_salones_semanal(fecha_descarga=fecha_descarga) if periodo == "semana" else exportar_xlsx_salones_mensual(fecha_descarga=fecha_descarga)
        else:
            return exportar_xlsx_reservaciones_semanal(fecha_descarga) if periodo == "semana" else exportar_xlsx_reservaciones_mensual(fecha_descarga)

    # === PDF ===
    if formato != "pdf":
        return HttpResponse("Formato no válido", status=400)

    if request.method != "POST":
        return HttpResponse("Use POST para generar PDF.", status=405)

    # Usuarios PDF
    if tipo == "usuarios":
        return exportar_pdf_usuarios_semanal(fecha_descarga=fecha_descarga) if periodo == "semana" else exportar_pdf_usuarios_mensual(fecha_descarga=fecha_descarga)

    # Salones PDF (usar exportar_pdf genérica como Reservaciones)
    elif tipo == "salones":
        from myapp.Descargas.export_pdf import exportar_pdf
        import io as io_module
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import calendar

        tz = pytz.timezone('America/Mexico_City')
        ref_date = timezone.localtime(timezone.now()).date()
        
        if periodo == "semana":
            inicio = ref_date - timedelta(days=ref_date.weekday())
            fin = inicio + timedelta(days=6)
        else:
            # MENSUAL: garantizar que cubre el mes completo
            inicio = ref_date.replace(day=1)
            last_day = calendar.monthrange(ref_date.year, ref_date.month)[1]
            fin = ref_date.replace(day=last_day)

        images = {}
        
        try:
            # Top 5 calificación
            top_cal = list(Salon.objects.values("nombre", "calificacion").order_by("-calificacion")[:5])
            labels_cal = [s["nombre"] for s in top_cal]
            vals_cal = [float(s.get("calificacion") or 0.0) for s in top_cal]
            
            fig, ax = plt.subplots(figsize=(8,4), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            ax.bar(labels_cal, vals_cal, color="#6366F1", edgecolor="#475569", linewidth=1.5)
            ax.set_title("Salones - Calificación", color="#E2E8F0", fontweight="bold")
            ax.tick_params(colors="#E2E8F0", rotation=30)
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='y')
            buf_cal = io_module.BytesIO()
            fig.savefig(buf_cal, format="png", bbox_inches="tight", dpi=150, facecolor="#0F172A")
            plt.close(fig)
            buf_cal.seek(0)
            img_cal_b64 = base64.b64encode(buf_cal.getvalue()).decode("ascii")
            images["calificacion"] = "data:image/png;base64," + img_cal_b64

            # Top 5 precios
            top_price = list(Salon.objects.values("nombre","precio").order_by("-precio")[:5])
            labels_price = [s["nombre"] for s in top_price]
            vals_price = [float(s.get("precio") or 0.0) for s in top_price]
            
            fig, ax = plt.subplots(figsize=(8,4), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            ax.bar(labels_price, vals_price, color="#3B82F6", edgecolor="#475569", linewidth=1.5)
            ax.set_title("Salones - Precio (MXN)", color="#E2E8F0", fontweight="bold")
            ax.tick_params(colors="#E2E8F0", rotation=30)
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='y')
            buf_price = io_module.BytesIO()
            fig.savefig(buf_price, format="png", bbox_inches="tight", dpi=150, facecolor="#0F172A")
            plt.close(fig)
            buf_price.seek(0)
            img_price_b64 = base64.b64encode(buf_price.getvalue()).decode("ascii")
            images["precios"] = "data:image/png;base64," + img_price_b64

            # Top 5 ingresos (TIMEZONE-AWARE)
            field_type = Reservacion._meta.get_field('fecha_reserva').get_internal_type()
            
            if field_type == "DateTimeField":
                # Convertir a datetime aware
                start_dt = datetime.combine(inicio, datetime.min.time())
                end_dt = datetime.combine(fin, datetime.max.time())
                
                # Localizar si no está localizado
                if start_dt.tzinfo is None:
                    start_dt = tz.localize(start_dt)
                if end_dt.tzinfo is None:
                    end_dt = tz.localize(end_dt)
                    
                qs_ing = Reservacion.objects.filter(fecha_reserva__range=[start_dt, end_dt])
            else:
                # DateField: usar rangos de fecha directamente
                qs_ing = Reservacion.objects.filter(fecha_reserva__range=[inicio, fin])

            top_ing = qs_ing.values("salon__nombre").annotate(total=Sum("precio_total")).order_by("-total")[:5]
            labels_ing = [s["salon__nombre"] for s in top_ing]
            vals_ing = [float(s.get("total") or 0.0) for s in top_ing]
            
            fig, ax = plt.subplots(figsize=(8,4), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            ax.bar(labels_ing, vals_ing, color="#22C55E", edgecolor="#475569", linewidth=1.5)
            ax.set_title("Salones - Ingresos (MXN)", color="#E2E8F0", fontweight="bold")
            ax.tick_params(colors="#E2E8F0", rotation=30)
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='y')
            buf_ing = io_module.BytesIO()
            fig.savefig(buf_ing, format="png", bbox_inches="tight", dpi=150, facecolor="#0F172A")
            plt.close(fig)
            buf_ing.seek(0)
            img_ing_b64 = base64.b64encode(buf_ing.getvalue()).decode("ascii")
            images["ingresos"] = "data:image/png;base64," + img_ing_b64

        except Exception as e:
            traceback.print_exc()
            print(f"Error generando imágenes: {e}")

        datos1_rows = [[s["nombre"], f"{float(s.get('calificacion') or 0.0):.2f}"] for s in top_cal]
        datos2_rows = [[s["nombre"], f"${float(s.get('precio') or 0.0):.2f}"] for s in top_price]
        datos3_rows = [[s["salon__nombre"], f"${float(s.get('total') or 0.0):.2f}"] for s in top_ing]

        charts_data = [
            {"nombre": "Salones con mejores reseñas", "tabla_headers": ["Salón","Calificación"], "tabla_rows": datos1_rows, "imagen": images.get("calificacion")},
            {"nombre": "Salones más caros", "tabla_headers": ["Salón","Precio (MXN)"], "tabla_rows": datos2_rows, "imagen": images.get("precios")},
            {"nombre": "Salones con más Ingresos", "tabla_headers": ["Salón","Ingresos (MXN)"], "tabla_rows": datos3_rows, "imagen": images.get("ingresos")},
        ]

        return exportar_pdf(charts_data, images, fecha_descarga=fecha_descarga, titulo_reporte=f"Salones - {'Semanal' if periodo=='semana' else 'Mensual'}")

    # Reservaciones PDF (default)
    else:
        if periodo == "semana":
            from myapp.Descargas.export_pdf import exportar_pdf_reservaciones_semanal
            return exportar_pdf_reservaciones_semanal(fecha_descarga=fecha_descarga)
        else:
            from myapp.Descargas.export_pdf import exportar_pdf_reservaciones_mensual
            return exportar_pdf_reservaciones_mensual(fecha_descarga=fecha_descarga)

@login_required
def descargar_comprobante_reserva(request, reserva_id):
    """Descarga el comprobante PDF de una reserva específica"""
    from django.shortcuts import get_object_or_404
    from myapp.models import Reservacion
    
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)
    
    # Preparar datos de la reserva
    charts_data = [
        {
            "nombre": "Detalles de la Reservación",
            "tabla_headers": ["Campo", "Valor"],
            "tabla_rows": [
                ["Salón", reserva.salon.nombre],
                ["Fecha", str(reserva.fecha_reserva)],
                ["Estado", reserva.estado],
                ["Precio Total", f"${reserva.precio_total}"],
            ]
        }
    ]
    
    tz = pytz.timezone('America/Mexico_City')
    now_local = timezone.now().astimezone(tz)
    fecha_descarga = now_local.strftime("%d/%m/%Y %H:%M:%S")
    
    return exportar_pdf(charts_data, {}, fecha_descarga=fecha_descarga, titulo_reporte=f"Comprobante - Reservación #{reserva.id}")


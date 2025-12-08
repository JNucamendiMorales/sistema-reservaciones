import io
import base64
from datetime import timedelta, datetime, time
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Sum
from myapp.models import Reservacion
import pytz
import json
from django.contrib.auth.models import User
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ===============================================================
# PDF - Función principal
# ===============================================================
def exportar_pdf(charts_data, images, fecha_descarga=None, titulo_reporte="Reporte"):
    """
    Genera un PDF en tema oscuro con tablas de datos ANTES de cada gráfica.
    """
    try:
        buffer = io.BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        def _new_page_with_background(title_text=None):
            pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
            pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
            pdf_canvas.setFillColorRGB(1, 1, 1)
            pdf_canvas.setFont("Helvetica-Bold", 16)
            pdf_canvas.drawCentredString(width / 2.0, height - 40, titulo_reporte)
            if fecha_descarga:
                pdf_canvas.setFont("Helvetica", 9)
                pdf_canvas.drawRightString(width - 40, height - 56, fecha_descarga)
            if title_text:
                pdf_canvas.setFont("Helvetica-Bold", 12)
                pdf_canvas.drawString(50, height - 80, title_text)

        y_position = height - 100
        first_page = True

        for idx, chart_data in enumerate(charts_data):
            if not first_page:
                pdf_canvas.showPage()
            first_page = False

            chart_name = chart_data.get("nombre", f"Gráfico {idx+1}")
            _new_page_with_background(chart_name)
            y_position = height - 100

            # ========== RENDERIZAR TABLA DE DATOS ==========
            if "tabla_headers" in chart_data and "tabla_rows" in chart_data:
                headers = chart_data["tabla_headers"]
                rows = chart_data["tabla_rows"]
                
                pdf_canvas.setFont("Helvetica-Bold", 10)
                pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
                
                col_width = (width - 100) / len(headers)
                
                # Encabezados
                for i, header in enumerate(headers):
                    x = 50 + (i * col_width)
                    pdf_canvas.drawString(x + 5, y_position, header)
                
                y_position -= 20
                pdf_canvas.setLineWidth(0.5)
                pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
                pdf_canvas.line(50, y_position, width - 50, y_position)
                
                # Filas de datos
                pdf_canvas.setFont("Helvetica", 9)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                
                for row in rows[:15]:  # Máximo 15 filas por tabla
                    y_position -= 15
                    for i, cell in enumerate(row):
                        x = 50 + (i * col_width)
                        pdf_canvas.drawString(x + 5, y_position, str(cell)[:30])
                    
                    if y_position < 100:
                        pdf_canvas.showPage()
                        _new_page_with_background(chart_name)
                        y_position = height - 100
                
                y_position -= 20

            # ========== RENDERIZAR GRÁFICA ==========
            img_raw = chart_data.get("imagen")
            
            if img_raw:
                try:
                    if isinstance(img_raw, str) and img_raw.startswith("data:"):
                        img_b64 = img_raw.split(",", 1)[1]
                    elif isinstance(img_raw, str):
                        img_b64 = img_raw
                    else:
                        img_b64 = None

                    if img_b64 is not None:
                        img_bytes = base64.b64decode(img_b64)
                    else:
                        img_bytes = img_raw

                    img_buffer = io.BytesIO(img_bytes)
                    img = ImageReader(img_buffer)
                    img_w, img_h = img.getSize()
                    max_w = width - 100
                    display_w = min(max_w, img_w)
                    display_h = display_w * (img_h / img_w)

                    max_h = height - 160
                    if display_h > max_h:
                        display_h = max_h
                        display_w = display_h * (img_w / img_h)

                    x = 50
                    y = y_position - display_h - 40
                    if y < 80:
                        pdf_canvas.showPage()
                        _new_page_with_background(chart_name)
                        y = height - 120 - display_h

                    pdf_canvas.drawImage(img, x, y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')

                except Exception as e:
                    print(f"Error al insertar imagen: {e}")
                    traceback.print_exc()
                    pdf_canvas.setFont("Helvetica", 10)
                    pdf_canvas.setFillColorRGB(1, 0, 0)
                    pdf_canvas.drawString(50, y_position - 20, f"[Error al insertar imagen: {str(e)[:50]}]")

        pdf_canvas.save()
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        return response

    except Exception as e:
        print(f"Error crítico en exportar_pdf: {e}")
        traceback.print_exc()
        raise ValueError(f"Error al generar PDF: {e}")


# ===============================================================
# PDF — Reservaciones por periodo (SEMANAL)
# ===============================================================
def exportar_pdf_reservaciones_semanal(fecha_descarga=None):
    """
    Genera PDF con datos de reservaciones semanales:
    - Tabla: Reservaciones por día
    - Tabla: Salones más reservados
    - Tabla: Ingresos por día
    """
    from django.db.models import Count, Sum
    import pytz
    
    tz = pytz.timezone('America/Mexico_City')
    hoy_local = timezone.now().astimezone(tz).date()
    inicio_semana = hoy_local - timedelta(days=hoy_local.weekday())
    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    conteos = []
    for i in range(7):
        d = inicio_semana + timedelta(days=i)
        total = Reservacion.objects.filter(fecha_reserva=d).count()
        conteos.append(total)

    por_salon_qs = Reservacion.objects.filter(
        fecha_reserva__range=[inicio_semana, inicio_semana + timedelta(days=6)]
    ).values("salon__nombre").annotate(total=Count("id")).order_by("-total")[:10]
    datos_salones = list(por_salon_qs)

    ingresos = []
    for i in range(7):
        d = inicio_semana + timedelta(days=i)
        total_ingreso = (Reservacion.objects
                         .filter(fecha_reserva=d)
                         .aggregate(total=Sum("precio_total"))["total"] or 0.0)
        ingresos.append(float(total_ingreso))

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Página 1: Reservaciones por día
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Reservaciones")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Reservaciones por Día")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Día")
    pdf_canvas.drawString(250, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_res = 0
    for nombre, valor in zip(dias_nombres, conteos):
        y -= 15
        pdf_canvas.drawString(60, y, nombre)
        pdf_canvas.drawString(250, y, str(valor))
        total_res += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(250, y, str(total_res))

    # Página 2: Salones
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Reservaciones")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Salones Más Reservados")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Salón")
    pdf_canvas.drawString(350, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_sal = 0
    for salon in datos_salones:
        y -= 15
        salon_name = salon["salon__nombre"][:40]
        pdf_canvas.drawString(60, y, salon_name)
        pdf_canvas.drawString(350, y, str(int(salon["total"])))
        total_sal += int(salon["total"])

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(350, y, str(total_sal))

    # -----------------------
    # Pie chart: Salones más reservados (semanal) - TEMA OSCURO + MÁS PEQUEÑO
    # -----------------------
    if datos_salones:
        labels = [s["salon__nombre"][:25] for s in datos_salones]
        sizes = [int(s["total"]) for s in datos_salones]
        
        palette = [
            "#6366F1", "#22C55E", "#EAB308", "#F97316", "#EF4444",
            "#3B82F6", "#A855F7", "#10B981", "#F59E0B", "#8B5CF6"
        ]
        
        pie_y = y - 150
        pie_height = 100  # MÁS PEQUEÑO
        
        if pie_y < 80:
            pdf_canvas.showPage()
            pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
            pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
            pdf_canvas.setFillColorRGB(1, 1, 1)
            pdf_canvas.setFont("Helvetica-Bold", 16)
            pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Reservaciones")
            if fecha_descarga:
                pdf_canvas.setFont("Helvetica", 9)
                pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
            pie_y = height - 150
        
        d = Drawing(180, pie_height)
        pie = Pie()
        pie.x = 10
        pie.y = 0
        pie.width = 90
        pie.height = pie_height
        pie.data = sizes
        pie.labels = None
        
        for i in range(len(sizes)):
            try:
                pie.slices[i].fillColor = colors.HexColor(palette[i % len(palette)])
            except Exception:
                pass
        
        d.add(pie)
        renderPDF.draw(d, pdf_canvas, 50, pie_y - pie_height)
        
        # Leyenda en tema oscuro
        legend_x = 250
        legend_y = pie_y
        pdf_canvas.setFont("Helvetica", 7)
        
        for i, label in enumerate(labels):
            color_hex = palette[i % len(palette)]
            r, g, b = int(color_hex[1:3], 16) / 255.0, int(color_hex[3:5], 16) / 255.0, int(color_hex[5:7], 16) / 255.0
            pdf_canvas.setFillColorRGB(r, g, b)
            pdf_canvas.rect(legend_x, legend_y - 10, 8, 8, fill=1, stroke=0)
            
            pdf_canvas.setFillColorRGB(0.95, 0.95, 0.95)
            pdf_canvas.drawString(legend_x + 12, legend_y - 6, label)
            
            legend_y -= 15
            if legend_y < 80:
                break

    # Página 3: Ingresos
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Reservaciones")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Ingresos por Día")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Día")
    pdf_canvas.drawString(250, y, "Ingresos ($)")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_ing = 0.0
    for nombre, valor in zip(dias_nombres, ingresos):
        y -= 15
        pdf_canvas.drawString(60, y, nombre)
        pdf_canvas.drawString(250, y, f"${valor:.2f}")
        total_ing += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(250, y, f"${total_ing:.2f}")

    pdf_canvas.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reservaciones_semanal.pdf"'
    return response


# ===============================================================
# PDF — Reservaciones por periodo (MENSUAL)
# ===============================================================
def exportar_pdf_reservaciones_mensual(fecha_descarga=None):
    """
    Genera PDF con datos de reservaciones mensuales:
    - Tabla: Reservaciones por rango de días
    - Tabla: Salones más reservados
    - Tabla: Ingresos por rango de días
    """
    from django.db.models import Count, Sum
    import pytz
    import calendar

    tz = pytz.timezone('America/Mexico_City')
    fecha_actual = timezone.now().astimezone(tz)
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    dias_rango = [
        (1, 5, "1-5"),
        (6, 10, "6-10"),
        (11, 15, "11-15"),
        (16, 20, "16-20"),
        (21, 25, "21-25"),
        (26, 31, "26-31"),
    ]

    # Conteos de reservaciones por rango (datetime-aware)
    conteos = []
    last_day = calendar.monthrange(año_actual, mes_actual)[1]
    for start, end, label in dias_rango:
        end_day = min(end, last_day)
        start_dt = datetime(año_actual, mes_actual, start, 0, 0, 0)
        end_dt = datetime(año_actual, mes_actual, end_day, 23, 59, 59, 999999)
        if start_dt.tzinfo is None:
            start_dt = tz.localize(start_dt)
        if end_dt.tzinfo is None:
            end_dt = tz.localize(end_dt)
        total = Reservacion.objects.filter(fecha_reserva__range=[start_dt, end_dt]).count()
        conteos.append((label, total))

    por_salon = list(
        Reservacion.objects
        .filter(fecha_reserva__year=año_actual, fecha_reserva__month=mes_actual)
        .values("salon__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    ingresos = []
    for start, end, label in dias_rango:
        total_ing = Reservacion.objects.filter(
            fecha_reserva__year=año_actual,
            fecha_reserva__month=mes_actual,
            fecha_reserva__day__gte=start,
            fecha_reserva__day__lte=end
        ).aggregate(total=Sum("precio_total"))["total"] or 0.0
        ingresos.append((label, float(total_ing)))

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    mes_str = fecha_actual.strftime('%B %Y')

    # Página 1: Reservaciones por período
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Reservaciones - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Reservaciones por Período")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Período")
    pdf_canvas.drawString(250, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_res = 0
    for label, valor in conteos:
        y -= 15
        pdf_canvas.drawString(60, y, label)
        pdf_canvas.drawString(250, y, str(valor))
        total_res += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(250, y, str(total_res))

    # Página 2: Salones
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Reservaciones - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Salones Más Reservados")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Salón")
    pdf_canvas.drawString(350, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_sal = 0
    for salon in por_salon:
        y -= 15
        salon_name = salon["salon__nombre"][:40]
        pdf_canvas.drawString(60, y, salon_name)
        pdf_canvas.drawString(350, y, str(int(salon["total"])))
        total_sal += int(salon["total"])

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(350, y, str(total_sal))

    # -----------------------
    # Pie chart: Salones más reservados (mensual) - TEMA OSCURO + MÁS PEQUEÑO
    # -----------------------
    if por_salon:
        labels = [s["salon__nombre"][:25] for s in por_salon]
        sizes = [int(s["total"]) for s in por_salon]
        
        palette = [
            "#6366F1", "#22C55E", "#EAB308", "#F97316", "#EF4444",
            "#3B82F6", "#A855F7", "#10B981", "#F59E0B", "#8B5CF6"
        ]
        
        pie_y = y - 150
        pie_height = 100  # MÁS PEQUEÑO
        
        if pie_y < 80:
            pdf_canvas.showPage()
            pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
            pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
            pdf_canvas.setFillColorRGB(1, 1, 1)
            pdf_canvas.setFont("Helvetica-Bold", 16)
            pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Reservaciones - {mes_str}")
            if fecha_descarga:
                pdf_canvas.setFont("Helvetica", 9)
                pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
            pie_y = height - 150
        
        d = Drawing(180, pie_height)
        pie = Pie()
        pie.x = 10
        pie.y = 0
        pie.width = 90
        pie.height = pie_height
        pie.data = sizes
        pie.labels = None
        
        for i in range(len(sizes)):
            try:
                pie.slices[i].fillColor = colors.HexColor(palette[i % len(palette)])
            except Exception:
                pass
        
        d.add(pie)
        renderPDF.draw(d, pdf_canvas, 50, pie_y - pie_height)
        
        # Leyenda en tema oscuro
        legend_x = 250
        legend_y = pie_y
        pdf_canvas.setFont("Helvetica", 7)
        
        for i, label in enumerate(labels):
            color_hex = palette[i % len(palette)]
            r, g, b = int(color_hex[1:3], 16) / 255.0, int(color_hex[3:5], 16) / 255.0, int(color_hex[5:7], 16) / 255.0
            pdf_canvas.setFillColorRGB(r, g, b)
            pdf_canvas.rect(legend_x, legend_y - 10, 8, 8, fill=1, stroke=0)
            
            pdf_canvas.setFillColorRGB(0.95, 0.95, 0.95)
            pdf_canvas.drawString(legend_x + 12, legend_y - 6, label)
            
            legend_y -= 15
            if legend_y < 80:
                break

    # Página 3: Ingresos
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Reservaciones - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Ingresos por Período")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Período")
    pdf_canvas.drawString(250, y, "Ingresos ($)")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_ing = 0.0
    for label, valor in ingresos:
        y -= 15
        pdf_canvas.drawString(60, y, label)
        pdf_canvas.drawString(250, y, f"${valor:.2f}")
        total_ing += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(250, y, f"${total_ing:.2f}")

    pdf_canvas.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reservaciones_mensual.pdf"'
    return response


# ===============================================================
# PDF — Usuarios semanal
# ===============================================================
def exportar_pdf_usuarios_semanal(fecha_descarga=None):
    from django.db.models import Count, Sum
    import pytz
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from datetime import datetime, time

    # FIX: usar zona local y rangos aware por día en lugar de __date
    tz = pytz.timezone('America/Mexico_City')
    hoy_local = timezone.now().astimezone(tz).date()
    inicio_semana = hoy_local - timedelta(days=hoy_local.weekday())
    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    nuevos = []
    for i in range(7):
        d = inicio_semana + timedelta(days=i)
        # crear bounds aware para ese día (00:00:00 .. 23:59:59.999999)
        start_dt = datetime.combine(d, time.min)
        end_dt = datetime.combine(d, time.max)
        if start_dt.tzinfo is None:
            start_dt = tz.localize(start_dt)
        if end_dt.tzinfo is None:
            end_dt = tz.localize(end_dt)
        total = User.objects.filter(date_joined__range=[start_dt, end_dt]).count()
        nuevos.append((dias_nombres[i], total))

    datos_activos = list(
        Reservacion.objects
        .filter(fecha_reserva__range=[inicio_semana, inicio_semana + timedelta(days=6)])
        .values("usuario__username")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    datos_ingresos = list(
        Reservacion.objects
        .filter(fecha_reserva__range=[inicio_semana, inicio_semana + timedelta(days=6)])
        .values("usuario__username")
        .annotate(total=Sum("precio_total"))
        .order_by("-total")[:10]
    )

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ========== PÁGINA 1: Tabla + PIE CHART - Usuarios nuevos ==========
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Nuevos usuarios registrados")

    # TABLA
    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Día")
    pdf_canvas.drawString(250, y, "Usuarios Nuevos")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_nuevos = 0
    for nombre, valor in nuevos:
        y -= 15
        pdf_canvas.drawString(60, y, nombre)
        pdf_canvas.drawRightString(430, y, str(valor))
        total_nuevos += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawRightString(430, y, str(total_nuevos))

    # PIE CHART debajo
    try:
        labels = [t[0] for t in nuevos]
        sizes = [t[1] for t in nuevos]
        if sum(sizes) > 0:
            fig, ax = plt.subplots(figsize=(7, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#0F172A")
            
            colors_palette = ["#4F46E5", "#22C55E", "#EAB308", "#F97316", "#EF4444", "#14B8A6", "#A855F7"]
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=None,
                colors=colors_palette[:len(sizes)],
                autopct="%1.1f%%",
                textprops={"color": "#E2E8F0", "fontsize": 8},
                wedgeprops={"edgecolor": "#0F172A", "linewidth": 1}
            )
            
            for autotext in autotexts:
                autotext.set_color("#E2E8F0")
                autotext.set_fontsize(8)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando pie chart:", e)

    # ========== PÁGINA 2: Tabla + HORIZONTAL BAR CHART - Usuarios activos ==========
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Usuarios con mas Reservaciones")

    # TABLA
    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Usuario")
    pdf_canvas.drawString(350, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_activos = 0
    for usuario in datos_activos:
        y -= 15
        user_name = usuario["usuario__username"][:40]
        pdf_canvas.drawString(60, y, user_name)
        pdf_canvas.drawRightString(430, y, str(int(usuario["total"])))
        total_activos += int(usuario["total"])

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawRightString(430, y, str(total_activos))

    # HORIZONTAL BAR CHART debajo
    try:
        labels = [u["usuario__username"][:20] for u in datos_activos]
        values = [int(u["total"]) for u in datos_activos]
        
        if any(values):
            fig, ax = plt.subplots(figsize=(8, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            
            ax.barh(labels, values, color="#3B82F6", edgecolor="#475569", linewidth=1)
            
            ax.set_xlabel("Reservaciones", color="#E2E8F0", fontsize=9)
            ax.tick_params(colors="#E2E8F0", labelsize=8)
            
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='x')
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando bar chart:", e)

    # ========== PÁGINA 3: Tabla + VERTICAL BAR CHART - Usuarios con mayores ingresos ==========
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Usuarios con mayores ingresos")

    # TABLA
    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Usuario")
    pdf_canvas.drawString(350, y, "Ingresos ($)")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_ing = 0.0
    for usuario in datos_ingresos:
        y -= 15
        user_name = usuario["usuario__username"][:40]
        valor = float(usuario["total"] or 0.0)
        pdf_canvas.drawString(60, y, user_name)
        pdf_canvas.drawRightString(430, y, f"${valor:.2f}")
        total_ing += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawRightString(430, y, f"${total_ing:.2f}")

    # VERTICAL BAR CHART debajo
    try:
        labels = [u["usuario__username"][:15] for u in datos_ingresos]
        values = [float(u["total"] or 0.0) for u in datos_ingresos]
        
        if any(values):
            fig, ax = plt.subplots(figsize=(8, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            
            ax.bar(labels, values, color="#22C55E", edgecolor="#475569", linewidth=1)
            
            ax.set_ylabel("Ingresos (MXN)", color="#E2E8F0", fontsize=9)
            ax.tick_params(colors="#E2E8F0", labelsize=8)
            
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='y')
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, "Reporte Semanal de Usuarios")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando ingresos chart:", e)

    pdf_canvas.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios_semanal.pdf"'
    return response


def exportar_pdf_usuarios_mensual(fecha_descarga=None):
    from django.db.models import Count, Sum
    import pytz
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import calendar
    from datetime import datetime, time

    tz = pytz.timezone('America/Mexico_City')
    fecha_actual = timezone.now().astimezone(tz)
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    dias_rango = [
        (1, 5, "1-5"),
        (6, 10, "6-10"),
        (11, 15, "11-15"),
        (16, 20, "16-20"),
        (21, 25, "21-25"),
        (26, 31, "26-31"),
    ]

    # Conteos de nuevos usuarios por rango (datetime-aware)
    conteos = []
    last_day = calendar.monthrange(año_actual, mes_actual)[1]
    for start, end, label in dias_rango:
        end_day = min(end, last_day)
        start_dt = datetime(año_actual, mes_actual, start, 0, 0, 0)
        end_dt = datetime(año_actual, mes_actual, end_day, 23, 59, 59, 999999)
        if start_dt.tzinfo is None:
            start_dt = tz.localize(start_dt)
        if end_dt.tzinfo is None:
            end_dt = tz.localize(end_dt)
        total = User.objects.filter(date_joined__range=[start_dt, end_dt]).count()
        conteos.append((label, total))

    usuarios_activos = list(
        Reservacion.objects.filter(
            fecha_reserva__year=año_actual,
            fecha_reserva__month=mes_actual
        ).values("usuario__username").annotate(total=Count("id")).order_by("-total")[:10]
    )

    usuarios_ingresos = list(
        Reservacion.objects.filter(
            fecha_reserva__year=año_actual,
            fecha_reserva__month=mes_actual
        ).values("usuario__username").annotate(total=Sum("precio_total")).order_by("-total")[:10]
    )

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    mes_str = fecha_actual.strftime('%B %Y')

    # Página 1: Tabla + PIE CHART - Nuevos usuarios (mensual)
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Nuevos usuarios registrados")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Período")
    pdf_canvas.drawString(250, y, "Usuarios Nuevos")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_nuevos = 0
    for label, valor in conteos:
        y -= 15
        pdf_canvas.drawString(60, y, label)
        pdf_canvas.drawString(250, y, str(valor))
        total_nuevos += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawString(250, y, str(total_nuevos))

    # Pie chart debajo
    try:
        labels = [t[0] for t in conteos]
        sizes = [t[1] for t in conteos]
        if sum(sizes) > 0:
            fig, ax = plt.subplots(figsize=(7, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#0F172A")
            
            colors_palette = ["#4F46E5", "#22C55E", "#EAB308", "#F97316", "#EF4444", "#14B8A6", "#A855F7"]
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=None,
                colors=colors_palette[:len(sizes)],
                autopct="%1.1f%%",
                textprops={"color": "#E2E8F0", "fontsize": 8},
                wedgeprops={"edgecolor": "#0F172A", "linewidth": 1}
            )
            
            for autotext in autotexts:
                autotext.set_color("#E2E8F0")
                autotext.set_fontsize(8)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando pie chart (mensual):", e)

    # Página 2: Tabla + HORIZONTAL BAR CHART - Usuarios con mas reservaciones (mensual)
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Usuarios con mas Reservaciones")

    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Usuario")
    pdf_canvas.drawString(350, y, "Reservaciones")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_activos = 0
    for usuario in usuarios_activos:
        y -= 15
        user_name = usuario["usuario__username"][:40]
        pdf_canvas.drawString(60, y, user_name)
        pdf_canvas.drawRightString(430, y, str(int(usuario["total"])))
        total_activos += int(usuario["total"])

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawRightString(430, y, str(total_activos))

    # HORIZONTAL BAR CHART debajo
    try:
        labels = [u["usuario__username"][:20] for u in usuarios_activos]
        values = [int(u["total"]) for u in usuarios_activos]
        
        if any(values):
            fig, ax = plt.subplots(figsize=(8, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            
            ax.barh(labels, values, color="#3B82F6", edgecolor="#475569", linewidth=1)
            
            ax.set_xlabel("Reservaciones", color="#E2E8F0", fontsize=9)
            ax.tick_params(colors="#E2E8F0", labelsize=8)
            
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='x')
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando bar chart:", e)

    # Página 3: Tabla + VERTICAL BAR CHART - Usuarios con mayores ingresos (mensual)
    pdf_canvas.showPage()
    pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
    pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
    if fecha_descarga:
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))

    pdf_canvas.setFont("Helvetica-Bold", 12)
    pdf_canvas.drawString(50, height - 100, "Usuarios con mayores ingresos")

    # TABLA
    y = height - 130
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.setFillColorRGB(0.3, 0.5, 0.8)
    pdf_canvas.drawString(60, y, "Usuario")
    pdf_canvas.drawString(350, y, "Ingresos ($)")

    y -= 20
    pdf_canvas.setLineWidth(0.5)
    pdf_canvas.setStrokeColorRGB(0.5, 0.5, 0.5)
    pdf_canvas.line(50, y, width - 50, y)

    pdf_canvas.setFont("Helvetica", 9)
    pdf_canvas.setFillColorRGB(1, 1, 1)
    total_ing = 0.0
    for usuario in usuarios_ingresos:
        y -= 15
        user_name = usuario["usuario__username"][:40]
        valor = float(usuario["total"] or 0.0)
        pdf_canvas.drawString(60, y, user_name)
        pdf_canvas.drawRightString(430, y, f"${valor:.2f}")
        total_ing += valor

    y -= 15
    pdf_canvas.drawString(60, y, "TOTAL")
    pdf_canvas.drawRightString(430, y, f"${total_ing:.2f}")

    # VERTICAL BAR CHART debajo
    try:
        labels = [u["usuario__username"][:15] for u in usuarios_ingresos]
        values = [float(u["total"] or 0.0) for u in usuarios_ingresos]
        
        if any(values):
            fig, ax = plt.subplots(figsize=(8, 3.5), facecolor="#0F172A")
            ax.set_facecolor("#1E293B")
            
            ax.bar(labels, values, color="#22C55E", edgecolor="#475569", linewidth=1)
            
            ax.set_ylabel("Ingresos (MXN)", color="#E2E8F0", fontsize=9)
            ax.tick_params(colors="#E2E8F0", labelsize=8)
            
            ax.spines['bottom'].set_color("#475569")
            ax.spines['left'].set_color("#475569")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.2, color="#475569", linestyle="--", axis='y')
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor="#0F172A")
            plt.close(fig)
            buf.seek(0)

            img = ImageReader(buf)
            img_w, img_h = img.getSize()
            max_w = width - 100
            display_w = min(max_w, img_w)
            display_h = display_w * (img_h / img_w)

            chart_x = 50
            chart_y = y - display_h - 30
            if chart_y < 80:
                pdf_canvas.showPage()
                pdf_canvas.setFillColorRGB(0.06, 0.09, 0.16)
                pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
                pdf_canvas.setFillColorRGB(1, 1, 1)
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawCentredString(width / 2.0, height - 40, f"Reporte Mensual de Usuarios - {mes_str}")
                if fecha_descarga:
                    pdf_canvas.setFont("Helvetica", 9)
                    pdf_canvas.drawRightString(width - 40, height - 56, str(fecha_descarga))
                chart_y = height - 200

            pdf_canvas.drawImage(img, chart_x, chart_y, width=display_w, height=display_h, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Error generando ingresos chart (mensual):", e)

    pdf_canvas.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios_mensual.pdf"'
    return response


# ===============================================================
# VISTAS / HELPERS
# ===============================================================
def generar_datos_para(charts):
    """Genera datos base para gráficas"""
    base_data = [
        {"Etiqueta": "Lunes", "Valor": 12},
        {"Etiqueta": "Martes", "Valor": 18},
        {"Etiqueta": "Miércoles", "Valor": 9},
        {"Etiqueta": "Jueves", "Valor": 14},
        {"Etiqueta": "Viernes", "Valor": 11},
        {"Etiqueta": "Sábado", "Valor": 16},
        {"Etiqueta": "Domingo", "Valor": 8},
    ]

    charts_data = []
    for name in charts:
        charts_data.append({
            "nombre": name.replace("_", " ").capitalize(),
            "datos": base_data
        })
    return charts_data


def descargar_pdf(request):
    """
    Recolección robusta de imágenes para generar PDF.
    """
    import json
    
    images = {}
    expected_keys = ["reservaciones", "salones_mas_reservados", "ingresos"]

    key_map = {
        "bar": "reservaciones",
        "pie": "salones_mas_reservados",
        "line": "ingresos",
    }

    if request.method == "POST":
        images_field = request.POST.get("images")
        if images_field:
            try:
                raw_images = json.loads(images_field)
                if isinstance(raw_images, dict):
                    for k, v in raw_images.items():
                        target = key_map.get(k, k)
                        if v:
                            images[target] = v
            except Exception:
                return HttpResponse("El campo 'images' debe contener JSON válido.", status=400)

        for alias, target in key_map.items():
            if target in images:
                continue
            val = request.POST.get(alias)
            if val:
                images[target] = val

    images = {k: v for k, v in images.items() if v}

    # Obtener tipo y período del request
    tipo = request.POST.get("tipo") or request.GET.get("tipo", "reservaciones")
    periodo = request.POST.get("periodo") or request.GET.get("periodo", "semana")
    fecha_descarga = request.POST.get("fecha") or request.GET.get("fecha")
    
    # Si es usuarios, generar PDF sin imágenes
    if tipo == "usuarios":
        if periodo == "semana":
            return exportar_pdf_usuarios_semanal(fecha_descarga=fecha_descarga)
        else:
            return exportar_pdf_usuarios_mensual(fecha_descarga=fecha_descarga)
    
    # Si es reservaciones, validar imágenes
    elif tipo == "reservaciones":
        missing = [k for k in expected_keys if k not in images]
        if missing:
            return HttpResponse(f"Faltan imágenes para: {', '.join(missing)}.", status=400)
        
        charts_param = request.POST.get("charts") or request.GET.get("charts", "")
        charts = charts_param.split(",") if charts_param else []
        if not charts:
            charts = ["Reservaciones", "Salones mas reservados", "Ingresos"]
        
        try:
            return exportar_pdf(generar_datos_para(charts), images, fecha_descarga=fecha_descarga)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return HttpResponse("Error al generar PDF", status=500)
    
    else:
        return HttpResponse("Tipo no soportado", status=400)
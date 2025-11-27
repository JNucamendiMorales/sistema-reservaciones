import io
import csv
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse,FileResponse
import base64
import io


def exportar_csv(charts_data):
    output = io.StringIO()
    writer = csv.writer(output)
    for chart in charts_data:
        writer.writerow([chart["nombre"]])
        writer.writerow(["Etiqueta", "Valor"])
        for fila in chart["datos"]:
            writer.writerow([fila["Etiqueta"], fila["Valor"]])
        writer.writerow([])  # blank line between charts
    response = HttpResponse(
        output.getvalue(),
        content_type="text/csv",
    )
    response["Content-Disposition"] = 'attachment; filename="graficas.csv"'
    return response


# ===============================================================
# Función auxiliar: datos de ejemplo
# ===============================================================
def generar_datos_para(charts):
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
    for chart_name in charts:
        charts_data.append({
            "nombre": chart_name.replace("_", " ").capitalize(),
            "datos": base_data
        })
    return charts_data

# ===============================================================
# CSV → solo tablas
# ===============================================================
def exportar_xlsx_nativo(charts_data):
    import io
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, PieChart, Reference
    from django.http import HttpResponse

    wb = Workbook()
    ws_default = wb.active
    wb.remove(ws_default)

    for chart in charts_data:
        ws = wb.create_sheet(title=chart["nombre"][:31])
        # Headers personalizados
        ws.append(["Mes", "No. reservaciones"])

        for fila in chart["datos"]:
            ws.append([fila.get("Etiqueta", ""), fila.get("Valor", "")])

        chart_name = chart["nombre"].lower()
        if "barras" in chart_name:
            c = BarChart()
            c.x_axis.title = "Mes"
            c.y_axis.title = "No. reservaciones"
        elif "líneas" in chart_name or "lineas" in chart_name:
            c = LineChart()
            c.x_axis.title = "Mes"
            c.y_axis.title = "No. reservaciones"
        elif "pastel" in chart_name or "pie" in chart_name:
            c = PieChart()
        else:
            c = BarChart()
            c.x_axis.title = "Mes"
            c.y_axis.title = "No. reservaciones"

        # Aquí ya no incluimos la fila de encabezado como parte de los datos
        data = Reference(ws, min_col=2, min_row=2, max_row=len(chart["datos"]) + 1)
        categories = Reference(ws, min_col=1, min_row=2, max_row=len(chart["datos"]) + 1)
        c.add_data(data, titles_from_data=False)  # No usar la primera fila como título
        c.set_categories(categories)
        c.title = chart["nombre"]
        ws.add_chart(c, "D2")

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="graficas.xlsx"'
    return response






def exportar_pdf(charts_data, images={}):
    import base64
    from reportlab.lib.utils import ImageReader

    # 👇 Insert a test image directly here
    dummy_image_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAUA"  # <-- you can use a longer real one
        "AAAFCAYAAACNbyblAAAAHElEQVQI12P4"
        "//8/w38GIAXDIBKE0DHxgljNBAAO"
        "9TXL0Y4OHwAAAABJRU5ErkJggg=="
    )
    if not images:
        images = {charts_data[0]["nombre"].lower(): dummy_image_base64}

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    for chart in charts_data:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, chart["nombre"])
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(60, y, "Etiqueta - Valor")
        y -= 15
        for fila in chart["datos"]:
            c.drawString(70, y, f"{fila['Etiqueta']} - {fila['Valor']}")
            y -= 15
            if y < 100:
                c.showPage()
                y = height - 50

        # Insert test image
        key = chart["nombre"].lower()
        if key in images:
            img_data = base64.b64decode(images[key])
            img = ImageReader(io.BytesIO(img_data))
            c.drawImage(img, 50, y-200, width=400, height=200)
            y -= 220

        y -= 25

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="graficas.pdf"'
    return response


# ===============================================================
# Vistas para Django
# ===============================================================
def descargar_csv(request):
    charts = request.GET.get("charts", "").split(",")
    charts_data = generar_datos_para(charts)
    return exportar_csv(charts_data)

def descargar_xlsx(request):
    charts = request.GET.get("charts", "").split(",")
    charts_data = generar_datos_para(charts)
    return exportar_xlsx_nativo(charts_data)

def descargar_pdf(request):
    import json
    charts = request.GET.get("charts", "").split(",")
    charts_data = generar_datos_para(charts)

    # Recibir imágenes base64
    images_json = request.GET.get("images", "{}")
    images = json.loads(images_json)  # {chart_name: base64}

    return exportar_pdf(charts_data, images)

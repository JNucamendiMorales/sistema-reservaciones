# Funciones para exportar CSV/XLSX/PDF

#imports
import csv
from django.http import HttpResponse
from myapp.models import Salon, Reservacion
from myapp.Descargas.export_charts import exportar_csv, exportar_pdf, exportar_xlsx_nativo




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
    """
    Permite descargar los gráficos en formato CSV, XLSX o PDF.
    Los datos se pueden reemplazar con datos reales más adelante.
    """
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

    # Seleccionar formato de exportación
    if formato == "csv":
        return exportar_csv(charts_data)
    elif formato == "xlsx":
        return exportar_xlsx_nativo(charts_data)
    elif formato == "pdf":
        return exportar_pdf(charts_data)
    else:
        return HttpResponse("Formato no válido", status=400)
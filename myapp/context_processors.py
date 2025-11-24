#Esto hace que reservaciones esté disponible en TODA la app, automáticamente.
from myapp.models import Reservacion
from django.utils.timezone import now

def reservaciones_usuario(request):
    if request.user.is_authenticated:
        todas = Reservacion.objects.filter(usuario=request.user).order_by("-fecha_reserva")
        proximas = todas.filter(fecha_reserva__gte=now())
        return {
            "reservaciones": todas,        # todas las reservaciones
            "proximas_reservaciones": proximas,  # solo próximas
        }
    return {
        "reservaciones": [],
        "proximas_reservaciones": []
    }

# Panel de admin y dashboards

#imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, F
from django.db.models.functions import ExtractMonth, ExtractWeek, TruncDate, TruncDay, TruncMonth
from django.utils.timezone import now, make_aware
from myapp.models import Salon, Reservacion,ServicioExtra
from myapp.forms import ReservacionAdminForm, SalonForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




# Dashboard principal
@staff_member_required
def admin_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_reservations": Reservacion.objects.count(),
        "total_salons": Salon.objects.count(),
        "recent_reservations": Reservacion.objects.order_by('-fecha_reserva')[:5]
    }
    return render(request, "admin_custom/dashboard.html", context)

# Listado de salones
def admin_salones(request):
    salones = Salon.objects.all().order_by('-id')
    return render(request, 'admin_custom/salones_admin.html', {'salones': salones})


# ---------- RESERVACIONES ----------
@staff_member_required
def admin_reservaciones(request):
    reservaciones = Reservacion.objects.select_related('usuario', 'salon').all().order_by('-fecha_reserva')
    return render(request, 'admin_custom/reservaciones_admin.html', {'reservaciones': reservaciones})

#USUARIOS
@staff_member_required
def usuarios_admin(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_custom/usuarios_admin.html', {'usuarios': usuarios})

def admin_usuarios_list(request):
    return render(request, 'admin_panel/usuarios_list.html')

def dashboard_view(request):
    # Totals
    total_salons = Salon.objects.count()
    total_reservations = Reservacion.objects.count()
    total_users = User.objects.count()

    # ✅ Chart 1: Reservations per month (MySQL compatible)
    reservations_by_month = (
        Reservacion.objects
        .annotate(month=ExtractMonth('fecha_reserva'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    months = [r['month'] for r in reservations_by_month]
    reservation_counts = [r['total'] for r in reservations_by_month]

    # ✅ Chart 2: Top 5 most booked salons
    top_salons = (
        Reservacion.objects
        .values('salon__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # ✅ Chart 3: New users per week (MySQL compatible)
    recent_users = (
        User.objects
        .annotate(week=ExtractWeek('date_joined'))
        .values('week')
        .annotate(total=Count('id'))
        .order_by('week')
    )
    weeks = [u['week'] for u in recent_users]
    user_counts = [u['total'] for u in recent_users]

    # ✅ Recent reservations table
    recent_reservations = Reservacion.objects.select_related('usuario', 'salon').order_by('-fecha_reserva')[:5]

    context = {
        'total_salons': total_salons,
        'total_reservations': total_reservations,
        'total_users': total_users,
        'months': months,
        'reservation_counts': reservation_counts,
        'top_salons': top_salons,
        'weeks': weeks,
        'user_counts': user_counts,
        'recent_reservations': recent_reservations,
    }

    return render(request, 'admin_custom/dashboard.html', context)





def admin_servicios_view(request):
    servicios = ServicioExtra.objects.all()
    return render(request, 'admin_custom/servicios_admin.html', {'servicios': servicios})






@csrf_exempt
def nuevo_servicio(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        precio = request.POST.get("precio", "0").strip()
        tipo_salon = request.POST.get("tipo_salon", "")
        imagen = request.FILES.get("imagen", None)

        errors = {}
        if not nombre:
            errors["nombre"] = ["Este campo es obligatorio."]
        if not precio or float(precio) < 0:
            errors["precio"] = ["Debe ser un número positivo."]
        if tipo_salon not in dict(ServicioExtra.TIPOS):
            errors["tipo_salon"] = ["Seleccione un tipo válido."]

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        servicio = ServicioExtra(
            nombre=nombre,
            precio=precio,
            tipo_salon=tipo_salon,
            imagen=imagen
        )
        servicio.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "errors": {"general": ["Método no permitido"]}})

@csrf_exempt
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(ServicioExtra, id=servicio_id)

    if request.method == "GET":
        # Enviar datos actuales para rellenar el modal
        return JsonResponse({
            "servicio": {
                "nombre": servicio.nombre,
                "precio": str(servicio.precio),
                "tipo_salon": servicio.tipo_salon,
            }
        })

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        precio = request.POST.get("precio", "0").strip()
        tipo_salon = request.POST.get("tipo_salon", "")
        imagen = request.FILES.get("imagen", None)

        errors = {}
        if not nombre:
            errors["nombre"] = ["Este campo es obligatorio."]
        if not precio or float(precio) < 0:
            errors["precio"] = ["Debe ser un número positivo."]
        if tipo_salon not in dict(ServicioExtra.TIPOS):
            errors["tipo_salon"] = ["Seleccione un tipo válido."]

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        servicio.nombre = nombre
        servicio.precio = precio
        servicio.tipo_salon = tipo_salon
        if imagen:
            servicio.imagen = imagen
        servicio.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "errors": {"general": ["Método no permitido"]}})

@csrf_exempt
def eliminar_servicio(request, servicio_id):
    if request.method == "POST":
        servicio = get_object_or_404(ServicioExtra, id=servicio_id)
        servicio.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": {"general": ["Método no permitido"]}})

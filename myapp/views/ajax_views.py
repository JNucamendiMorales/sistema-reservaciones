# Vistas que retornan JsonResponse

#imports
import json
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from myapp.models import Salon, Reservacion
from myapp.serializers import SalonSerializer, ReservacionSerializer
from myapp.forms import ReservacionAdminForm,SalonForm,RegistroForm
from rest_framework import viewsets
from datetime import datetime, timedelta  # para manejo normal de fechas
from django.utils.timezone import now, make_aware  # funciones de Django para fechas con zona horaria




# Crear salón--------------------------------------------------------------------------
@csrf_exempt
@staff_member_required
def salon_create(request):
    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            salon = form.save()
            salon_dict = model_to_dict(salon)
            # ✅ Convert ImageField to URL so it's serializable
            salon_dict['imagen'] = salon.imagen.url if salon.imagen else ''
            return JsonResponse({
                'success': True,
                'message': 'Salón creado exitosamente.',
                'salon': salon_dict
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
# Editar salón--------------------------------------------------------------------------
@csrf_exempt
@staff_member_required
def salon_edit(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES, instance=salon)
        if form.is_valid():
            salon = form.save()
            data = model_to_dict(salon)
            data['imagen'] = salon.imagen.url if salon.imagen else ''
            return JsonResponse({
                'success': True,
                'message': 'Salón actualizado correctamente.',
                'salon': data
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    # Si es GET (cuando haces clic en "Editar")
    data = model_to_dict(salon)
    data['imagen'] = salon.imagen.url if salon.imagen else ''
    return JsonResponse({'success': True, 'salon': data})


# Eliminar salón-----------------------------------------------------------------------------
@csrf_exempt
@staff_member_required
def salon_delete(request, salon_id):
    if request.method == 'POST':
        salon = get_object_or_404(Salon, id=salon_id)
        salon.delete()
        return JsonResponse({'success': True, 'message': 'Salón eliminado correctamente.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


#Info del salon-------------------------------------------------------------------------------- 
def salon_info(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
        return JsonResponse({
            "success": True,
            "nombre": salon.nombre,
            "precio": salon.precio,
        })
    except Salon.DoesNotExist:
        return JsonResponse({"success": False}, status=404)
    
#Crear reservacion--------------------------------------------------------------------    
@csrf_exempt
@staff_member_required
def reservacion_create(request):
    if request.method == 'POST':
        form = ReservacionAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método inválido'})


#Edita la reservacion---------------------------------------------------------------------
@csrf_exempt
@staff_member_required
def reservacion_edit(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)
    if request.method == 'GET':
        data = {
            'usuario': reservacion.usuario.id,
            'salon': reservacion.salon.id,
            'fecha_reserva': reservacion.fecha_reserva,
            'estado': reservacion.estado,
            'precio_total': reservacion.precio_total,
        }
        return JsonResponse({'success': True, 'data': data})
    elif request.method == 'POST':
        form = ReservacionAdminForm(request.POST, instance=reservacion)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método inválido'})


#Elimina la reservacion-------------------------------------------------------------------------
@csrf_exempt
@staff_member_required
def reservacion_delete(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)
    reservacion.delete()
    return JsonResponse({'success': True})


#Crea un usuario
@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'success': True, 'user': model_to_dict(user)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
        
        
#Elimina un usuario
@csrf_exempt
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': True})
    
# 1) TOP 5 MEJORES CALIFICADOS
def top_calificacion(request):
    salones = Salon.objects.all().order_by('-calificacion')[:5]
    data = [
        {"nombre": s.nombre, "calificacion": float(s.calificacion)}
        for s in salones
    ]
    return JsonResponse(data, safe=False)



# 2) TOP 5 MÁS CAROS
def top_precio(request):
    salones = Salon.objects.all().order_by('-precio')[:5]
    data = [
        {"nombre": s.nombre, "precio": float(s.precio)}
        for s in salones
    ]
    return JsonResponse(data, safe=False)



# 3) TOP 5 INGRESOS (SEMANAL/MENSUAL)
def top_ingresos(request):
    periodo = request.GET.get("periodo", "semana")
    modo = request.GET.get("modo", "mejores")

    hoy = datetime.now().date()

    if periodo == "semana":
        fecha_inicio = hoy - timedelta(days=7)
    elif periodo == "mes":
        fecha_inicio = hoy - timedelta(days=30)
    else:
        return JsonResponse({"error": "Parámetro 'periodo' inválido"}, status=400)

    ingresos = (
        Reservacion.objects
        .filter(fecha_reserva__gte=fecha_inicio, pagada=True)
        .values("salon__id", "salon__nombre")
        .annotate(total=Sum("precio_total"))
    )

    if not ingresos:
        labels = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"] if periodo == "semana" else \
                 ["01–05","06–10","11–15","16–20","21–25","26–31"]

        return JsonResponse({
            "labels": labels,
            "series": [
                {"salon": "-", "data": [0] * len(labels)} for _ in range(5)
            ]
        })

    ingresos = sorted(
        ingresos,
        key=lambda x: x["total"],
        reverse=(modo == "mejores")
    )[:5]

    if periodo == "semana":
        labels = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
        series = []

        for item in ingresos:
            salon_id = item["salon__id"]
            salon_name = item["salon__nombre"]

            dias = [0] * 7

            reservas = Reservacion.objects.filter(
                salon__id=salon_id,
                fecha_reserva__gte=fecha_inicio,
                pagada=True
            )

            for r in reservas:
                idx = r.fecha_reserva.weekday()
                dias[idx] += float(r.precio_total)

            series.append({
                "salon": salon_name,
                "data": dias
            })

        return JsonResponse({"labels": labels, "series": series})

    elif periodo == "mes":
        labels = ["01–05","06–10","11–15","16–20","21–25","26–31"]
        series = []

        for item in ingresos:
            salon_id = item["salon__id"]
            salon_name = item["salon__nombre"]

            rangos = [0] * 6

            reservas = Reservacion.objects.filter(
                salon__id=salon_id,
                fecha_reserva__gte=fecha_inicio,
                pagada=True
            )

            for r in reservas:
                d = r.fecha_reserva.day
                total = float(r.precio_total)

                if d <= 5: rangos[0] += total
                elif d <= 10: rangos[1] += total
                elif d <= 15: rangos[2] += total
                elif d <= 20: rangos[3] += total
                elif d <= 25: rangos[4] += total
                else: rangos[5] += total

            series.append({
                "salon": salon_name,
                "data": rangos
            })

        return JsonResponse({"labels": labels, "series": series})
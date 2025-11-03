import json
from .models import Salon,Reservacion,Reservacion,Favorito
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse,HttpResponse
#from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from .serializers import SalonSerializer, ReservacionSerializer
from rest_framework import viewsets
from datetime import datetime,timedelta
from .forms import RegistroForm,ReservacionForm
from decimal import Decimal
#from weasyprint import HTML
#from xhtml2pdf import pisa
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter

# Create your views here.

#Inicio.html----------------------------------------------------------

def pagina_inicio(request):
    # Filtra salones de tendencia
    tendencia = Salon.objects.filter(calificacion__gte=4.6)

    # Filtra salones más cercanos
    mas_cercanos = Salon.objects.filter(ciudad="CDMX")

    context = {
        'tendencia': tendencia,
        'mas_cercanos': mas_cercanos
    }

    return render(request, "theme/inicio.html", context )

#filtrar_categoria.html------------------------------------------------

def filtrar_categoria(request, categoria):
    salones = Salon.objects.filter(categoria__iexact=categoria)
    context = {
        'salones': salones,
        'categoria': categoria.capitalize(),
    }
    return render(request, 'theme/salones_categoria.html', context)

#filtrar salones en el navbar
def filtrar_salon(request):
    salones = Salon.objects.all()

    ciudad = request.GET.get('ciudad')
    capacidad = request.GET.get('capacidad')
    categoria = request.GET.get('categoria')
    precio = request.GET.get('precio')
    calificacion = request.GET.get('calificacion')

    if ciudad:
        salones = salones.filter(ciudad__iexact=ciudad)

    if capacidad:
        # Filtramos salones con capacidad >= valor seleccionado
        try:
            capacidad_int = int(capacidad)
            salones = salones.filter(capacidad__gte=capacidad_int)
        except ValueError:
            pass

    if categoria:
        salones = salones.filter(categoria__iexact=categoria)

    if precio:
        # Precio viene como "min-max" o "min+"
        if '+' in precio:
            try:
                min_precio = int(precio.replace('+', ''))
                salones = salones.filter(precio__gte=min_precio)
            except ValueError:
                pass
        else:
            try:
                rango = precio.split('-')
                min_precio = int(rango[0])
                max_precio = int(rango[1])
                salones = salones.filter(precio__gte=min_precio, precio__lte=max_precio)
            except (ValueError, IndexError):
                pass

    if calificacion:
        try:
            calificacion_int = int(calificacion)
            salones = salones.filter(calificacion__gte=calificacion_int)
        except ValueError:
            pass

    contexto = {
        'salones': salones,
        'filtros': {
            'ciudad': ciudad,
            'capacidad': capacidad,
            'categoria': categoria,
            'precio': precio,
            'calificacion': calificacion,
        }
    }
    return render(request, 'theme/listar_salones.html', contexto)




#detalle_salon.html-----------------------------------------------------

def detalle_salon(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    favorito = None
    if request.user.is_authenticated:
        favorito = Favorito.objects.filter(usuario=request.user, salon=salon).exists()
    return render(request, 'theme/salon_detalle.html', {'salon': salon, 'favorito': favorito})


#Hacer registro-------------------------------------------------------------------------------

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'theme/registro.html', {'form': form})


#obliga a iniciar sesion---------------------------------------------------------------------------

@login_required
def reservar_salon(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    reservas = Reservacion.objects.filter(salon=salon).values_list('fecha_reserva', flat=True)
    fechas_reservadas = [fecha.strftime('%Y-%m-%d') for fecha in reservas]

    return render(request, 'theme/reservar.html', {
        'salon': salon,
        'fechas_reservadas': json.dumps(fechas_reservadas),
    })

#Hacer reserva (formulario)

def reservar(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')  # o donde quieras redirigir
    else:
        form = ReservacionForm()
    return render(request, 'theme/reservar.html', {'form': form})


#Mostrar fechas ocupadas------------------------------------------------------------------------------------------------
@login_required
def reserva_view(request, salon_id):
    salon = get_object_or_404(Salon, pk=salon_id)
    reservas = Reservacion.objects.filter(salon=salon).values_list('fecha_reserva', flat=True)
    fechas_reservadas = [fecha.strftime('%Y-%m-%d') for fecha in reservas]

    return render(request, 'theme/reservar.html', {
        'salon': salon,
        'fechas_reservadas': fechas_reservadas,
    })


#función dedicada para recibir el POST AJAX---------------------------------------------------------------------------
@login_required
def crear_reserva(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    if request.method == 'POST':
        fecha_str = request.POST.get('fecha_reserva')
        if not fecha_str:
            # Manejo de error si no viene fecha
            return render(request, 'theme/resumen_reserva.html', {
                'salon': salon,
                'error': 'Fecha no proporcionada',
            })

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'theme/resumen_reserva.html', {
                'salon': salon,
                'error': 'Formato de fecha inválido',
            })

        # Verificar si ya está reservada
        if Reservacion.objects.filter(salon=salon, fecha_reserva=fecha).exists():
            return render(request, 'theme/resumen_reserva.html', {
                'salon': salon,
                'error': 'La fecha ya está reservada',
            })

        reserva = Reservacion.objects.create(
            salon=salon,
            usuario=request.user,
            fecha_reserva=fecha,
            estado='pendiente'
        )

        # Asignar precio total basado en el precio del salón
        reserva.precio_total = salon.precio
        reserva.save()

        return redirect('vista_pago', reserva_id=reserva.id)

    # Si no es POST, redirigir o mostrar error
    return JsonResponse({'error': 'Método no permitido'}, status=405)




#Hacer pago------------------------------------------------------------------------------------------------------------------
@login_required
def vista_pago(request, reserva_id):
    reserva = get_object_or_404(Reservacion, id=reserva_id)
    salon = reserva.salon

    # Si reserva tiene precio_total lo usamos, si no usamos precio del salón
    total_original = Decimal(reserva.precio_total) if reserva.precio_total else Decimal(salon.precio)
    codigo_ingresado = ''
    descuento_aplicado = Decimal('0')
    total_final = total_original

    context = {
        "reserva": reserva,
        "salon": salon,
        "precio_original_por_dia": salon.precio,
        "total_original": total_original,
        "total": total_original,       # total sin descuento
        "total_final": total_final,    # total con descuento (igual al original acá)
        "codigo_ingresado": codigo_ingresado,
        "descuento_aplicado": descuento_aplicado,
    }
    return render(request, "theme/pago.html", context)


#Vista de procesar pago----------------------------------------------------------------------------------------------------------
@login_required
def procesar_pago(request):
    if request.method != "POST":
        return redirect('home')

    reserva_id = request.POST.get("reserva_id")
    if not reserva_id:
        return redirect('home')

    reserva = get_object_or_404(Reservacion, id=reserva_id)
    salon = reserva.salon

    total_original = Decimal(reserva.precio_total) if reserva.precio_total else Decimal(salon.precio)

    codigo = request.POST.get("codigo_descuento", "").strip()
    aplicar_descuento = request.POST.get("aplicar_descuento")
    realizar_pago = request.POST.get("realizar_pago")

    descuento_aplicado = Decimal('0')
    total = total_original

    if aplicar_descuento:
        if codigo.lower() == "pongame10":
            descuento_aplicado = total * Decimal('0.10')
            total = total - descuento_aplicado

        context = {
            "reserva": reserva,
            "salon": salon,
            "precio_original_por_dia": salon.precio,
            "total_original": total_original,
            "total": total,
            "total_final": total,
            "descuento_aplicado": descuento_aplicado,
            "codigo_ingresado": codigo,
        }
        return render(request, "theme/pago.html", context)

    elif realizar_pago:
        if codigo.lower() == "pongame10":
            descuento_aplicado = total * Decimal('0.10')
            total = total - descuento_aplicado

        reserva.pagada = True
        reserva.save()

        request.session['total_final'] = str(total)
        request.session['descuento_aplicado'] = str(descuento_aplicado)
        request.session['codigo_ingresado'] = codigo

        return redirect('confirmacion_pago', reserva_id=reserva.id)

    return redirect('vista_pago', reserva_id=reserva.id)


#Mi perfil-----------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render

@login_required
def mi_perfil(request):
    return render(request, 'theme/mi_perfil.html')


#Resumen de la reserva para despues pagar-----------------------------------------------------------------------------------------
@login_required
def resumen_reserva(request, salon_id, fecha):
    salon = get_object_or_404(Salon, pk=salon_id)
    fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()

    reserva, creada = Reservacion.objects.get_or_create(
        salon=salon,
        usuario=request.user,
        fecha_reserva=fecha_reserva,
        defaults={
            'estado': 'pendiente',
            'pagada': False
        }
    )

    precio_original = Decimal(salon.precio)
    descuento_aplicado = Decimal('0')
    total_final = precio_original
    codigo_ingresado = ''

    if request.method == "POST" and 'codigo_descuento' in request.POST:
        codigo_ingresado = request.POST.get('codigo_descuento', '').strip()
        if codigo_ingresado.lower() == 'pongame10':
            descuento_aplicado = (precio_original * Decimal('0.10')).quantize(Decimal('0.01'))
            total_final = (precio_original - descuento_aplicado).quantize(Decimal('0.01'))

    # Guardar precio total actualizado en la reserva
    reserva.precio_total = total_final
    reserva.save()

    contexto = {
        'reserva': reserva,
        'salon': salon,
        'fecha_reserva': fecha_reserva,
        'precio_original_por_dia': precio_original,
        'total_original': precio_original,
        "total": total_final,
        'descuento_aplicado': descuento_aplicado,
        'total_final': total_final,
        'codigo_ingresado': codigo_ingresado,
    }
    return render(request, 'theme/pago.html', contexto)

#Confirmacion del pago---------------------------------------------------------------------------------------------------------------------
@login_required
def confirmacion_pago(request, reserva_id):
    reserva = get_object_or_404(Reservacion, id=reserva_id)

    # Asegurar que la reserva esté pagada
    if not reserva.pagada:
        return redirect('vista_pago', reserva_id=reserva_id)

    total_final = request.session.get('total_final', None)
    descuento_aplicado = request.session.get('descuento_aplicado', None)
    codigo_ingresado = request.session.get('codigo_ingresado', '')

    contexto = {
        'reserva': reserva,
        'total_final': total_final,
        'descuento_aplicado': descuento_aplicado,
        'codigo_ingresado': codigo_ingresado,
    }
    return render(request, 'theme/confirmacion_pago.html', contexto)


#listado de mis reservas------------------------------------------------------------------------------------------------------------------

@login_required
def mis_reservaciones(request):
    reservaciones = Reservacion.objects.filter(usuario=request.user).order_by('-fecha_reserva')
    return render(request, 'theme/mis_reservaciones.html', {'reservaciones': reservaciones})


#listado de mis favoritos--------------------------------------------------------------------------------------------------------------------

@login_required
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('salon')
    context = {
        'favoritos': favoritos,
    }
    return render(request, 'theme/mis_favoritos.html', context)

#boton de desactivar/activar favorito------------------------------------------------------------------------------------------------------------
@login_required
@require_POST
def toggle_favorito(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    usuario = request.user

    favorito, created = Favorito.objects.get_or_create(usuario=usuario, salon=salon)
    if not created:
        favorito.delete()
        estado = "eliminado"
    else:
        estado = "agregado"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "estado": estado})
    else:
        return JsonResponse({"success": False, "error": "Solo AJAX permitido"})

#Elimnar reservacion---------------------------------------------------------------------------------------------
@login_required
def eliminar_reservacion(request, reserva_id):
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reservación eliminada correctamente.")
        return redirect('mis_reservaciones')

    # Si quieres puedes mostrar una página de confirmación aquí, pero con el confirm JS en el botón basta.
    return redirect('mis_reservaciones')





def lista_salones(request):
    salones = Salon.objects.filter(disponible=True)
    return render(request, 'salones/lista_salones.html', {'salones': salones})

@login_required
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            reservacion = form.save(commit=False)
            reservacion.usuario = request.user
            reservacion.estado = 'pendiente'
            reservacion.save()
            return redirect('lista_salones')  # O donde quieras redirigir después
    else:
        form = ReservacionForm()

    return render(request, 'reservaciones/crear_reservacion.html', {'form': form})




def home_view(request):
    return render(request, "theme/home.html")


#Endpoints

class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

class ReservacionViewSet(viewsets.ModelViewSet):
    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
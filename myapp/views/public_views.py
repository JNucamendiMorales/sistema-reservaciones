"""
Vistas públicas accesibles para usuarios normales:
Inicio, listar salones, filtros, favoritos, reservas, pagos, perfil.
"""

# ===========================
# Imports
# ===========================
import json
from datetime import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from datetime import date

from myapp.models import Salon, Reservacion, Favorito, ServicioExtra
from myapp.forms import ReservacionForm


# ===========================
# Home / Listado / Filtros
# ===========================

def pagina_inicio(request):
    """Página principal con salones recientes, tendencia y más cercanos."""
    context = {
        'recientes': Salon.objects.order_by('-created_at')[:10],
        'tendencia': Salon.objects.filter(calificacion__gte=4.6),
        'mas_cercanos': Salon.objects.filter(ciudad="CDMX"),
    }
    return render(request, "theme/inicio.html", context)




from django.db.models import Max,Min





def lista_salones(request):
    salones = Salon.objects.all()

    # ==========================
    # 1. CATEGORÍA POR DEFECTO
    # ==========================
    default_categoria = request.GET.get('default_categoria')
    categorias_seleccionadas = request.GET.getlist('categoria')

    # Si el usuario llegó desde el navbar con ?default_categoria=X
    if default_categoria and default_categoria not in categorias_seleccionadas:
        categorias_seleccionadas.append(default_categoria)

    # Aplicamos filtro de categorías
    if categorias_seleccionadas:
        salones = salones.filter(categoria__in=categorias_seleccionadas)

    # ==========================
    # 2. CIUDADES DINÁMICAS
    # ==========================
    ciudades = Salon.objects.values_list('ciudad', flat=True).distinct()
    ciudades_seleccionadas = request.GET.getlist('ciudad')
    if ciudades_seleccionadas:
        salones = salones.filter(ciudad__in=ciudades_seleccionadas)

    # ==========================
    # 3. CAPACIDAD
    # ==========================
    capacidad_min = request.GET.get('capacidad_min')
    capacidad_max = request.GET.get('capacidad_max')
    if capacidad_min:
        salones = salones.filter(capacidad__gte=capacidad_min)
    if capacidad_max:
        salones = salones.filter(capacidad__lte=capacidad_max)

    # ==========================
    # 4. PRECIOS
    # ==========================
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        salones = salones.filter(precio__gte=precio_min)
    if precio_max:
        salones = salones.filter(precio__lte=precio_max)

    # ==========================
    # 5. MAX/MIN DESDE BD
    # ==========================
    capacidad_max_db = Salon.objects.aggregate(Max('capacidad'))['capacidad__max'] or 0
    capacidad_min_db = Salon.objects.aggregate(Min('capacidad'))['capacidad__min'] or 0
    precio_max_db = Salon.objects.aggregate(Max('precio'))['precio__max'] or 0
    precio_min_db = Salon.objects.aggregate(Min('precio'))['precio__min'] or 0

    # ==========================
    # CONTEXTO
    # ==========================
    context = {
        'salones': salones,
        'categorias': Salon.CATEGORIAS,
        'categorias_seleccionadas': categorias_seleccionadas,

        'ciudades': ciudades,
        'ciudades_seleccionadas': ciudades_seleccionadas,

        'capacidad_min_db': capacidad_min_db,
        'capacidad_max_db': capacidad_max_db,
        'precio_min_db': precio_min_db,
        'precio_max_db': precio_max_db,

        'default_categoria': default_categoria,
    }

    return render(request, 'theme/salones.html', context)



def filtrar_categoria(request, categoria):
    """Filtra salones por categoría."""
    salones = Salon.objects.filter(categoria__iexact=categoria)
    return render(request, 'theme/salones_categoria.html', {
        'salones': salones,
        'categoria': categoria.capitalize(),
    })


def filtrar_salon(request):
    """Filtrado avanzado desde el navbar (ciudad, capacidad, categoría, precio, calificación)."""
    salones = Salon.objects.all()

    ciudad = request.GET.get('ciudad')
    capacidad = request.GET.get('capacidad')
    categoria = request.GET.get('categoria')
    precio = request.GET.get('precio')
    calificacion = request.GET.get('calificacion')

    if ciudad:
        salones = salones.filter(ciudad__iexact=ciudad)

    if capacidad:
        try:
            salones = salones.filter(capacidad__gte=int(capacidad))
        except ValueError:
            pass

    if categoria:
        salones = salones.filter(categoria__iexact=categoria)

    if precio:
        try:
            if '+' in precio:
                salones = salones.filter(precio__gte=int(precio.replace('+', '')))
            else:
                min_p, max_p = map(int, precio.split('-'))
                salones = salones.filter(precio__gte=min_p, precio__lte=max_p)
        except Exception:
            pass

    if calificacion:
        try:
            salones = salones.filter(calificacion__gte=int(calificacion))
        except ValueError:
            pass

    return render(request, 'theme/listar_salones.html', {
        'salones': salones,
        'filtros': {
            'ciudad': ciudad,
            'capacidad': capacidad,
            'categoria': categoria,
            'precio': precio,
            'calificacion': calificacion,
        }
    })


# ===========================
# Detalle de salón
# ===========================

def detalle_salon(request, salon_id):
    """Detalle individual del salón con favoritos y servicios extra."""
    salon = get_object_or_404(Salon, id=salon_id)
    favorito = Favorito.objects.filter(usuario=request.user, salon=salon).exists() if request.user.is_authenticated else None

    servicios_extras = ServicioExtra.objects.filter(tipo_salon=salon.categoria)

    return render(request, 'theme/salon_detalle.html', {
        'salon': salon,
        'favorito': favorito,
        'servicios_extras': servicios_extras,
        'steps_list': ["Salón", "Extras", "Revisión", "Pago"],
        'current_step': 1,
        'step_width': 0,
        'MEDIA_URL': settings.MEDIA_URL,
    })


# ===========================
# Reservas (selección, extras, revisión)
# ===========================

@login_required
def reserva_view(request, salon_id):
    """Mostrar fechas ocupadas en el calendario."""
    salon = get_object_or_404(Salon, pk=salon_id)
    reservas = Reservacion.objects.filter(salon=salon).values_list('fecha_reserva', flat=True)

    return render(request, 'theme/reservar.html', {
        'salon': salon,
        'fechas_reservadas': [f.strftime('%Y-%m-%d') for f in reservas],
    })


import json
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import Salon, Reservacion

@login_required
def reservar_salon(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    # Crear o recuperar sesión temporal de reserva
    temp = request.session.get('reserva_temp', {})
    temp['salon_id'] = salon.id

    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if not fecha:
            messages.error(request, "Debes seleccionar una fecha.")
            return redirect('reservar', salon_id=salon_id)
        
        # Validar formato
        try:
            _ = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de fecha inválido.")
            return redirect('reservar', salon_id=salon_id)

        # Guardar fecha en sesión
        temp['fecha'] = fecha
        request.session['reserva_temp'] = temp
        request.session.modified = True

        # Redirigir a extras
        return redirect('seleccionar_extras', salon_id=salon_id)

    # Guardar sesión inicial
    request.session['reserva_temp'] = temp
    request.session.modified = True

    # Obtener fechas reservadas y convertir a JSON válido
    reservas = Reservacion.objects.filter(salon=salon).values_list('fecha_reserva', flat=True)
    fechas_reservadas = [f.strftime('%Y-%m-%d') for f in reservas]
    fechas_reservadas_json = json.dumps(fechas_reservadas)  # <-- CORRECCIÓN

    return render(request, 'theme/reservar.html', {
        'salon': salon,
        'fechas_reservadas': fechas_reservadas_json,  # <-- enviar JSON válido
    })






@login_required
def seleccionar_extras(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    temp = request.session.get('reserva_temp')
    if not temp or temp.get('salon_id') != salon.id or not temp.get('fecha'):
        return redirect('reservar', salon_id=salon.id)

    # Formatear fecha a dd-mm-yyyy
    fecha_reserva = temp.get('fecha')
    try:
        fecha_formateada = datetime.strptime(fecha_reserva, '%Y-%m-%d').strftime('%d-%m-%Y')
    except ValueError:
        fecha_formateada = fecha_reserva  # fallback por si hay error

    extras_disponibles = ServicioExtra.objects.filter(tipo_salon=salon.categoria)

    if request.method == "POST":
        extras_ids = request.POST.getlist('extras')
        temp['extras'] = list(map(int, extras_ids))
        request.session['reserva_temp'] = temp
        request.session.modified = True

        return redirect('pago')

    return render(request, 'theme/seleccionar_extras.html', {
        'salon': salon,
        'extras_disponibles': extras_disponibles,
        'reserva': {'fecha_reserva': fecha_formateada}  # <-- fecha ya en dd-mm-yyyy
    })









@login_required
def revision_reserva(request, reserva_id):
    """Paso 3: Revisión final antes de pagar."""
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)
    return render(request, 'theme/revision.html', {
        'reserva': reserva,
        'current_step': 3,
    })


# ===========================
# Pago (resumen, procesar, confirmar)
# ===========================

#Esta es la vista principal del checkout — donde el usuario: Ve el salón, Ve la fecha, Ve los extras seleccionados, Ve el total a pagar, Puede aplicar el código de descuento, Puede realizar el pago
@login_required
def pago(request):
    temp = request.session.get('reserva_temp')

    # Validar inicio del flujo
    if not temp or 'fecha' not in temp or 'salon_id' not in temp:
        return redirect('reservacion_resumen_view', reserva_id=reserva.id)

    salon = get_object_or_404(Salon, id=temp['salon_id'])
    fecha_reserva = datetime.strptime(temp['fecha'], '%Y-%m-%d').date()
    extras_ids = temp.get('extras', [])

    # ===============================
    #  PRECIOS BASE Y EXTRAS
    # ===============================
    precio_original_por_dia = Decimal(salon.precio)

    precio_extras = sum(
        ServicioExtra.objects.filter(id__in=extras_ids)
        .values_list('precio', flat=True)
    )

    # Lista de extras seleccionados (IMPORTANTE)
    extras_seleccionados = ServicioExtra.objects.filter(id__in=extras_ids)

    # Total sin descuento (salón + extras)
    total_original = precio_original_por_dia + precio_extras

    descuento_aplicado = Decimal('0')
    codigo_ingresado = ""

    # ===============================
    #  PROCESAR CÓDIGO DESCUENTO
    # ===============================
    if request.method == "POST" and "aplicar_descuento" in request.POST:

        codigo_ingresado = request.POST.get("codigo_descuento", "").strip()

        if codigo_ingresado.lower() == "pongame10":
            descuento_aplicado = (total_original * Decimal('0.10')).quantize(Decimal("0.01"))

        total_final = total_original - descuento_aplicado

        return render(request, "theme/pago.html", {
            "salon": salon,
            "fecha_reserva": fecha_reserva,
            "precio_original_por_dia": precio_original_por_dia,
            "precio_extras": precio_extras,
            "extras_seleccionados": extras_seleccionados,   # <--- AGREGADO
            "total_original": total_original,
            "total_final": total_final,
            "descuento_aplicado": descuento_aplicado,
            "codigo_ingresado": codigo_ingresado,
            "reserva": None,
        })

    # ===============================
    #  PROCESAR PAGO Y CREAR RESERVA
    # ===============================
    if request.method == "POST" and "realizar_pago" in request.POST:

        codigo_ingresado = request.POST.get("codigo_descuento", "").strip()

        if codigo_ingresado.lower() == "pongame10":
            descuento_aplicado = (total_original * Decimal('0.10')).quantize(Decimal("0.01"))

        total_final = total_original - descuento_aplicado

        # Crear reserva
        reserva = Reservacion.objects.create(
            usuario=request.user,
            salon=salon,
            fecha_reserva=fecha_reserva,
            estado='confirmada',
            precio_total=total_final
        )
        reserva.servicios_extra.set(extras_ids)

        # Limpiar sesión
        if 'reserva_temp' in request.session:
            del request.session['reserva_temp']

        return redirect('reservacion_resumen_view', reserva_id=reserva.id)

    # ===============================
    #  ENTRADA NORMAL A LA PÁGINA
    # ===============================
    return render(request, "theme/pago.html", {
    "salon": salon,
    "fecha_reserva": fecha_reserva,
    "precio_original_por_dia": precio_original_por_dia,
    "precio_extras": precio_extras,
    "extras_seleccionados": extras_seleccionados,
    "total_original": total_original,
    "total_final": total_original,
    "descuento_aplicado": descuento_aplicado,
    "codigo_ingresado": codigo_ingresado,
})




@login_required
def pago_extra(request, reserva_id):
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)

    # Validación de tiempo
    hoy = date.today()
    dias_faltantes = (reserva.fecha_reserva - hoy).days

    if dias_faltantes < 2:
        return render(request, 'theme/pago_extra_bloqueado.html', {
            'reserva': reserva,
            'dias_faltantes': dias_faltantes
        })

    # Obtener todos los extras disponibles
    extras_disponibles = ServicioExtra.objects.all()

    if request.method == "POST":
        extras_ids = request.POST.getlist('extras')

        # Calcular precio extra
        precio_extras = sum(
            ServicioExtra.objects.filter(id__in=extras_ids)
            .values_list('precio', flat=True)
        )

        # Sumar al total existente
        reserva.precio_total += Decimal(precio_extras)
        reserva.save()

        # Asociar nuevos extras
        reserva.servicios_extra.add(*extras_ids)

        return redirect('reservacion_resumen_view', reserva_id=reserva.id)

    return render(request, 'theme/pago_extra.html', {
        'reserva': reserva,
        'extras_disponibles': extras_disponibles,
    })




@login_required
def resumen_reserva(request, reserva_id):
    """Muestra el resumen final después de pagar."""
    
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)

    salon = reserva.salon
    extras_seleccionados = reserva.servicios_extra.all()

    return render(request, 'theme/resumen_reserva.html', {
        'reserva': reserva,
        'salon': salon,
        'extras_seleccionados': extras_seleccionados,
        'precio_original_por_dia': salon.precio,
        'precio_extras': sum(extra.precio for extra in extras_seleccionados),
        'total_final': reserva.precio_total,
    })



@login_required
def vista_pago(request, reserva_id):
    """Página de pago principal."""
    reserva = get_object_or_404(Reservacion, id=reserva_id)
    salon = reserva.salon

    total = Decimal(reserva.precio_total) if reserva.precio_total else Decimal(salon.precio)

    return render(request, "theme/pago.html", {
        "reserva": reserva,
        "salon": salon,
        "total_original": total,
        "total_final": total,
        "descuento_aplicado": Decimal('0'),
        "codigo_ingresado": "",
        "current_step": 4,
    })





@login_required
def reservacion_resumen_view(request, reserva_id):
    """Pantalla final después del pago."""
    reserva = get_object_or_404(Reservacion, id=reserva_id)
    
    # Calcular subtotal extras
    subtotal_extras = sum(extra.precio for extra in reserva.servicios_extra.all())
    
    # Obtener descuento y código de la sesión
    descuento_aplicado = Decimal(str(request.session.get('descuento_aplicado', 0)))
    codigo_ingresado = request.session.get('codigo_ingresado', '')

    return render(request, 'theme/resumen_reserva.html', {
        'reserva': reserva,
        'total_final': reserva.precio_total,
        'descuento_aplicado': descuento_aplicado,
        'codigo_ingresado': codigo_ingresado,
    })



# ===========================
# Mis reservaciones
# ===========================

@login_required
def mis_reservaciones(request):
    res = Reservacion.objects.filter(usuario=request.user).order_by('-fecha_reserva')
    return render(request, 'theme/mis_reservaciones.html', {'reservaciones': res})


@login_required
def ver_mi_reservacion(request, reserva_id):
    reservacion = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)
    return render(request, 'theme/ver_mi_reservacion.html', {
        'reservacion': reservacion
    })


@login_required
def eliminar_reservacion(request, reserva_id):
    reserva = get_object_or_404(Reservacion, id=reserva_id, usuario=request.user)

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reservación eliminada correctamente.")

    return redirect('mis_reservaciones')


# ===========================
# Favoritos
# ===========================

@login_required
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('salon')
    # Extraer solo los salones
    salones_favoritos = [f.salon for f in favoritos]
    return render(request, 'theme/mis_favoritos.html', {'salones_favoritos': salones_favoritos})



@login_required
@require_POST
def toggle_favorito(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    usuario = request.user

    favorito, created = Favorito.objects.get_or_create(usuario=usuario, salon=salon)
    estado = "agregado" if created else "eliminado"

    if not created:
        favorito.delete()

    return JsonResponse({"success": True, "estado": estado})


# ===========================
# Perfil
# ===========================

from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from myapp.models import Reservacion

from datetime import date, timedelta
from calendar import monthrange

@login_required
def mi_perfil(request):
    usuario = request.user
    profile = usuario.profile

    # ------------------------
    # LISTA COMPLETA DE RESERVACIONES
    # ------------------------
    todas_reservaciones = (
        Reservacion.objects
        .filter(usuario=usuario)
        .select_related("salon")
        .prefetch_related("servicios_extra")
        .order_by("-fecha_reserva")
    )

    # ------------------------
    # FECHAS
    # ------------------------
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    # Mes anterior
    if hoy.month == 1:
        inicio_mes_anterior = date(hoy.year - 1, 12, 1)
    else:
        inicio_mes_anterior = date(hoy.year, hoy.month - 1, 1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)

    # ------------------------
    # FILTRAR RESERVACIONES PAGADAS
    # ------------------------
    # Mes actual
    reservaciones_mes = todas_reservaciones.filter(fecha_reserva__gte=inicio_mes)

    # Mes anterior
    reservaciones_mes_anterior = todas_reservaciones.filter(
        pagada=True,
        fecha_reserva__gte=inicio_mes_anterior,
        fecha_reserva__lte=fin_mes_anterior
    )

    # ------------------------
    # GASTOS EN SALONES
    # ------------------------
    gasto_salon_mes = sum(reserva.salon.precio for reserva in reservaciones_mes)
    gasto_salon_anterior = sum(reserva.salon.precio for reserva in reservaciones_mes_anterior)

    # ------------------------
    # GASTOS EN SERVICIOS EXTRA
    # ------------------------
    gasto_servicios_mes = sum(
        sum(extra.precio for extra in reserva.servicios_extra.all())
        for reserva in reservaciones_mes
    )
    gasto_servicios_anterior = sum(
        sum(extra.precio for extra in reserva.servicios_extra.all())
        for reserva in reservaciones_mes_anterior
    )

    # ------------------------
    # CALCULAR PORCENTAJES
    # ------------------------
    def calcular_porcentaje(actual, anterior):
        if anterior == 0:
            return 100 if actual > 0 else 0
        return round(((actual - anterior) / anterior) * 100, 2)

    pct_salon = calcular_porcentaje(gasto_salon_mes, gasto_salon_anterior)
    pct_servicios = calcular_porcentaje(gasto_servicios_mes, gasto_servicios_anterior)

    # ------------------------
    # CONTEXTO PARA LA PLANTILLA
    # ------------------------
    context = {
        'usuario': usuario,
        'profile': profile,
        'reservaciones': todas_reservaciones,  # lista completa
        'stats': {
            'gasto_salon': {
                'total': round(gasto_salon_mes, 2),
                'texto': "Este mes",
                'porcentaje': pct_salon
            },
            'gasto_servicios': {
                'total': round(gasto_servicios_mes, 2),
                'texto': "Este mes",
                'porcentaje': pct_servicios
            }
        }
    }    
         # ------------------------
    # DATOS PARA GRÁFICO DE ACTIVIDAD
    # ------------------------
    actividad=[]
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    dias_mes = (hoy - inicio_mes).days + 1

    for dia in range(1, dias_mes + 1):
        fecha_actual = inicio_mes.replace(day=dia)
        reservas_dia = reservaciones_mes.filter(fecha_reserva=fecha_actual)
    
        total_dia = sum(float(reserva.salon.precio) for reserva in reservas_dia)
        total_dia += sum(sum(float(extra.precio) for extra in reserva.servicios_extra.all())
                        for reserva in reservas_dia)
    
        actividad.append({
            "dia": dia,
            "total": total_dia
        })

    context['actividad_json'] = json.dumps(actividad)

    return render(request, 'theme/mi_perfil.html', context)






# ===========================
# Utilidades
# ===========================

def home_view(request):
    return render(request, "theme/home.html")







def help_view(request):
    return render(request, "help.html")

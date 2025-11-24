#vistas que requieren login o manipulan datos del usuario (crear_reserva, registro, login/logout, etc.).
# Login, registro, logout

#imports
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.forms import RegistroForm,Salon,Reservacion
from datetime import datetime, timedelta  # para manejo normal de fechas
from django.utils.timezone import now, make_aware  # funciones de Django para fechas con zona horaria
from django.urls import reverse



@login_required
def editar_perfil(request):
    usuario = request.user
    profile = usuario.profile

    if request.method == "POST":

        # === Campos de User (solo si quieres editar username y email) ===
        username = request.POST.get("username")
        email = request.POST.get("email")

        if username:
            usuario.username = username
        if email:
            usuario.email = email

        usuario.save()

        # === Campos de Profile ===
        profile.full_name = request.POST.get("full_name", profile.full_name)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.address = request.POST.get("address", profile.address)
        profile.gender = request.POST.get("genero", profile.gender)

        birth_date = request.POST.get("birth_date")
        if birth_date:
            profile.birth_date = birth_date

        # === Foto ===
        if "foto" in request.FILES:
            profile.avatar = request.FILES["foto"]

        profile.save()

        messages.success(request, "Tu perfil ha sido actualizado correctamente.")
        return redirect("mi_perfil")

    return redirect("mi_perfil")





def registro(request):
    next_url = request.GET.get("next", "")  # <- recuperamos el next si existe

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor inicia sesión.')

            # Si existe next, mandarlo al login con ?next=...
            if next_url:
                return redirect(f"{reverse('login')}?next={next_url}")

            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'theme/registro.html', {
        'form': form,
        'next': next_url,   # <- opcional si lo quieres poner en el formulario
    })


#Revisa si el usuario tiene permisos de admin
@login_required
def login_redirect_view(request):
    user = request.user
    
    # 1) Ver si existe una URL previa guardada
    next_url = request.session.pop('next_url', None)

    # 2) Si existe next_url, regresa ahí
    if next_url:
        return redirect(next_url)

    # 3) Si es admin → pantalla de elegir modo
    if user.is_staff or user.is_superuser:
        return render(request, 'theme/choose_mode.html', {'user': user})

    # 4) Usuario normal → inicio
    return redirect('inicio')


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    Logs out the user and redirects to 'inicio' (home).
    Prefer POST from templates for safety — but allow GET if needed.
    """
    if request.method == "POST" or request.method == "GET":
        logout(request)
        return redirect('inicio')
    return redirect('inicio')


def choose_mode(request):
    # Revisamos si había una next_url en sesión
    next_url = request.session.pop('next_url', None)

    modo = request.GET.get('modo')

    if modo == 'usuario':
        # Si había next → redirigir
        if next_url:
            return redirect(next_url)
        return redirect('inicio')

    elif modo == 'admin':
        if next_url:
            return redirect(next_url)
        return redirect('admin_dashboard')  # ajusta esto si usas otra vista

    # Mostrar la plantilla por default
    return render(request, 'theme/choose_mode.html')


#login para el admin
def login_view(request):
    # Si ya está logueado, respeta redirect según permisos
    if request.user.is_authenticated:
        return login_redirect_view(request)

    form = AuthenticationForm(request, data=request.POST or None)

    # Capturar el next desde GET o POST
    next_url = (
        request.GET.get('next') or 
        request.POST.get('next')
    )

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Guardar next temporal si existe
            if next_url:
                request.session['next_url'] = next_url

            return login_redirect_view(request)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'theme/login.html', {
        "form": form,
        "next": next_url  # para mantener next en el formulario
    })




#logout para el admin
def admin_logout_view(request):
    logout(request)
    return redirect('inicio')


#función dedicada para recibir el POST AJAX---------------------------------------------------------------------------
@login_required
def crear_reserva(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Datos enviados desde pago.html
    salon_id = request.POST.get('salon_id')
    fecha_str = request.POST.get('fecha')
    extras_ids = request.POST.getlist('extras')

    salon = get_object_or_404(Salon, id=salon_id)

    # Convertir fecha
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except:
        return render(request, 'theme/resumen_reserva.html', {
            'error': 'Fecha inválida',
            'salon': salon
        })

    # Verificar si ya está reservada
    if Reservacion.objects.filter(salon=salon, fecha_reserva=fecha).exists():
        return render(request, 'theme/resumen_reserva.html', {
            'error': 'La fecha ya está reservada',
            'salon': salon
        })

    # Calcular total
    total = salon.precio
    extras_obj = []

    for e in extras_ids:
        extra = ExtraServicio.objects.get(id=e)
        extras_obj.append(extra)
        total += extra.precio

    # Crear reservación al hacer clic en pagar
    reserva = Reservacion.objects.create(
        salon=salon,
        usuario=request.user,
        fecha_reserva=fecha,
        precio_total=total,
        estado="Confirmada"  # 🔥 Default como tú lo quieres
    )

    # Agregar extras M2M
    reserva.extras.set(extras_obj)

    # Ir al resumen
    return redirect('resumen_reserva', reserva_id=reserva.id)

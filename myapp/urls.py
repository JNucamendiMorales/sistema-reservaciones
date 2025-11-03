from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import registro, filtrar_categoria,detalle_salon,reservar_salon,SalonViewSet, ReservacionViewSet
from myapp.views import pagina_inicio

router = DefaultRouter()
router.register(r'api/salones', SalonViewSet, basename='salon')
router.register(r'api/reservaciones', ReservacionViewSet, basename='reservacion')

urlpatterns = [
    path('', pagina_inicio, name='inicio'),  # Welcome
    path('home/', views.home_view, name='home'),  # After login
    path('lista-salones/', views.lista_salones, name='lista_salones'),
    path('reservar/', views.crear_reservacion, name='crear_reservacion'),
    
    #menu desplegable de perfil
    path('mis-reservaciones/', views.mis_reservaciones, name='mis_reservaciones'),
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),

    #boton de toggle favorito
    path('favorito/toggle/<int:salon_id>/', views.toggle_favorito, name='toggle_favorito'),

    #Ver detalles del salon
    path('salon/<int:salon_id>/', detalle_salon, name='detalle_salon'),

    # Filtrar categorias (navbar)
    path('categoria/<str:categoria>/', filtrar_categoria, name='filtrar_categoria'),

    #Filtrar salones (navbar)
    path('filtrar/', views.filtrar_salon, name='filtrar_salon'),


    #Reservar salon
    path('salon/<int:salon_id>/reservar/', views.reservar_salon, name='reservar_salon'),
    path('salon/<int:salon_id>/crear_reserva/', views.crear_reserva, name='crear_reserva'),

    #En mis reservas (elimnar una reservacion)
    path('reservacion/eliminar/<int:reserva_id>/', views.eliminar_reservacion, name='eliminar_reservacion'),

    #Registro de usuario
    path('registro/', registro, name='registro'),

    #Inspeccionar perfil
    path('perfil/', views.mi_perfil, name='mi_perfil'),

    #Resumen de reserva
    path('salon/<int:salon_id>/resumen/<fecha>/', views.resumen_reserva, name='resumen_salon_fecha'),

    #Pagos
    path('pago/<int:reserva_id>/', views.vista_pago, name='vista_pago'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),

    path('confirmacion/<int:reserva_id>/', views.confirmacion_pago, name='confirmacion_pago'),

    #resumen
    path('resumen/reserva/<int:reserva_id>/', views.resumen_reserva, name='resumen_reserva'),
    path('resumen/<int:salon_id>/<str:fecha>/', views.resumen_reserva, name='resumen_salon_fecha_2'),

    #Descargar PDF
    #path('reserva/<int:reserva_id>/comprobante/', views.descargar_comprobante_pdf, name='descargar_comprobante_pdf'),

    #path('comprobante/<int:reserva_id>/', views.descargar_comprobante, name='descargar_comprobante'),



    # Rutas de la API REST
    path('', include(router.urls)),
]






from django.urls import path, include
from rest_framework.routers import DefaultRouter

# --- Public views ---
from myapp.views.public_views import (
    pagina_inicio,
    filtrar_salon,
    reservar_salon,
    filtrar_categoria,
    detalle_salon,
    seleccionar_extras,
    vista_pago,
    home_view,
    lista_salones,
    mis_reservaciones,
    mis_favoritos,
    toggle_favorito,
    eliminar_reservacion,
    mi_perfil,
    help_view,
    ver_mi_reservacion,
    pago,
    pago_extra,resumen_reserva,
    reservacion_resumen_view
)

# --- Auth views ---
from myapp.views.auth_views import (
    registro, login_redirect_view, choose_mode,
    admin_logout_view, crear_reserva, login_view,
    logout_view,editar_perfil
)

# --- Admin views ---
from myapp.views.admin_views import (
    admin_dashboard, admin_salones, admin_reservaciones,
    usuarios_admin, dashboard_view,admin_servicios_view,nuevo_servicio,
    editar_servicio,eliminar_servicio
)

# --- Export / Descargas ---
from myapp.views.export_views import descargar_reportes, dashboard_export
from myapp.Descargas import export_charts

# --- Chart / API views ---
from myapp.views.chart_views import (
    chart_reservaciones, chart_usuarios, chart_salones,
    obtener_datos_reservaciones, obtener_datos_usuarios, obtener_datos_salones
)

# --- AJAX / Top views ---
from myapp.views.ajax_views import (
    top_calificacion, top_precio, top_ingresos,
    crear_usuario, eliminar_usuario, salon_create,
    salon_edit, salon_delete, salon_info,
    reservacion_create, reservacion_edit, reservacion_delete
)

# --- DRF ViewSets ---
from myapp.views.api_views import SalonViewSet, ReservacionViewSet,search_salones


# --- Router DRF ---
router = DefaultRouter()
router.register(r'api/salones', SalonViewSet, basename='salon')
router.register(r'api/reservaciones', ReservacionViewSet, basename='reservacion')


urlpatterns = [

    # ======================================================
    # ===================== FRONTEND =======================
    # ======================================================
    path('', pagina_inicio, name='inicio'),
    path('home/', home_view, name='home'),
    path('lista-salones/', lista_salones, name='lista_salones'),

    # --- Usuario ---
    path('mis_reservaciones/', mis_reservaciones, name='mis_reservaciones'),
    path('mis_reservaciones/<int:reserva_id>/', ver_mi_reservacion, name='ver_mi_reservacion'),
    path('mis-favoritos/', mis_favoritos, name='mis_favoritos'),
    path('favorito/toggle/<int:salon_id>/', toggle_favorito, name='toggle_favorito'),
    path('reservacion/eliminar/<int:reserva_id>/', eliminar_reservacion, name='eliminar_reservacion'),
    path('mi_perfil/', mi_perfil, name='mi_perfil'),
    path('ayuda/', help_view, name='help'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),

    # --- Salones y búsqueda ---
    path('salon/<int:salon_id>/', detalle_salon, name='detalle_salon'),
    path('categoria/<str:categoria>/', filtrar_categoria, name='filtrar_categoria'),
    path('filtrar/', filtrar_salon, name='filtrar_salon'),

    # ======================================================
    # ====== NUEVO FLUJO COMPLETO DE RESERVACIONES ========
    # ======================================================

    # Paso 1: Seleccionar fecha
    path('salon/<int:salon_id>/reservar/', reservar_salon, name='reservar'),
    
    # Paso 2: Seleccionar extras
    path('salon/<int:salon_id>/extras/', seleccionar_extras, name='seleccionar_extras'),
    
    # Paso 3: Resumen de pago (aún sin crear reserva)
    path('pago/', pago, name='pago'),

    
    path('pago/vista/<int:reserva_id>/', vista_pago, name='vista_pago'),


    path('pago/proceso/<int:reserva_id>/', pago, name='proceso_pago'),

    
    path('pago-extra/<int:reserva_id>/', pago_extra, name='pago_extra'),
    

    
    path('salon/<int:salon_id>/pago/', vista_pago, name='vista_pago_nuevo'),

    # Paso 4: Procesar pago (crear reserva o pagar diferencia)
    path('procesar_pago/', pago, name='procesar_pago'),

    # Paso 5: Resumen de la reserva (ya se creó la reservación)
    path('resumen-reserva/<int:reserva_id>/', reservacion_resumen_view, name='reservacion_resumen_view'),




    # ======================================================
    # ==================== LOGIN / AUTH ====================
    # ======================================================
    path('login/', login_view, name='login'),
    path('logout/', admin_logout_view, name='logout'),
    path('login-redirect/', login_redirect_view, name='login_redirect'),
    path('choose-mode/', choose_mode, name='choose_mode'),
    path('registro/', registro, name='registro'),


    # ======================================================
    # ===================== ADMIN AREA ======================
    # ======================================================
    path('admin/', admin_dashboard, name='admin'),
    path('admin/usuarios/', usuarios_admin, name='admin_usuarios_list'),
    path('admin/usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('admin/usuarios/eliminar/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),

    path('admin/salones/', admin_salones, name='admin_salones'),
    path('admin/salones/nuevo/', salon_create, name='salon_create'),
    path('admin/salones/editar/<int:salon_id>/', salon_edit, name='salon_edit'),
    path('admin/salones/eliminar/<int:salon_id>/', salon_delete, name='salon_delete'),
    path('admin/salon-info/<int:salon_id>/', salon_info, name='salon_info'),

    path('admin/reservaciones/', admin_reservaciones, name='admin_reservaciones'),
    path('admin/reservaciones/nueva/', reservacion_create, name='reservacion_create'),
    path('admin/reservaciones/editar/<int:reservacion_id>/', reservacion_edit, name='reservacion_edit'),
    path('admin/reservaciones/eliminar/<int:reservacion_id>/', reservacion_delete, name='reservacion_delete'),
    
    path('admin/servicios/', admin_servicios_view, name='servicios_admin'),
    path('admin/servicios/nuevo/', nuevo_servicio, name='nuevo_servicio'),
    path('admin/servicios/editar/<int:servicio_id>/', editar_servicio, name='editar_servicio'),
    path('admin/servicios/eliminar/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),

    path('admin/dashboard/', dashboard_view, name='dashboard_view'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/export/', dashboard_export, name='dashboard_export'),
    
    


    # ======================================================
    # ===================== CHARTS API =====================
    # ======================================================
    path('admin/chart_reservaciones/', chart_reservaciones, name='chart_reservaciones'),
    path('admin/chart_usuarios/', chart_usuarios, name='chart_usuarios'),
    path('admin/chart_salones/', chart_salones, name='chart_salones'),

    path('api/reservaciones/datos/', obtener_datos_reservaciones, name='obtener_datos_reservaciones'),
    path('api/datos_usuarios/', obtener_datos_usuarios, name='obtener_datos_usuarios'),
    path('api/datos_salones/', obtener_datos_salones, name='obtener_datos_salones'),
    path('api/salones/top-calificacion/', top_calificacion, name='top_calificacion'),
    path('api/salones/top-precio/', top_precio, name='top_precio'),
    path('api/salones/top-ingresos/', top_ingresos, name='top_ingresos'),
    
    #=======================================================
    #===================== Search bar ======================
    #=======================================================
    
    path("api/search/", search_salones, name="search_salones"),

    # ======================================================
    # ==================== DESCARGAS ========================
    # ======================================================
    path('descargar/<str:formato>/', descargar_reportes, name='descargar_reportes'),
    path('descargar/csv/', export_charts.descargar_csv, name='descargar_csv'),
    path('descargar/xlsx/', export_charts.descargar_xlsx, name='descargar_xlsx'),
    path('descargar/pdf/', export_charts.descargar_pdf, name='descargar_pdf'),
    
    # NUEVO — RESERVACIONES SEMANAL
    path('descargar/periodo/', export_charts.descargar_reservaciones_periodo, name='descargar_reservaciones_periodo'),

    # ======================================================
    # ===================== DRF ROUTER =====================
    # ======================================================
    path('', include(router.urls)),
]

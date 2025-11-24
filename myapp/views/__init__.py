# --- Public views ---
from .public_views import (
    pagina_inicio, 
    filtrar_salon, filtrar_categoria,
    detalle_salon,
    seleccionar_extras,
    reservar_salon,
    vista_pago,
)

# --- Auth views ---
from .auth_views import (
    registro, login_redirect_view, choose_mode,
    admin_logout_view, crear_reserva, login_view,
    logout_view
)

# --- Admin views ---
from .admin_views import (
    admin_dashboard, admin_salones,
    admin_reservaciones, dashboard_view,
    usuarios_admin
)

# --- Export views ---
from .export_views import descargar_reportes, dashboard_export

# --- Chart views ---
from .chart_views import (
    chart_reservaciones, chart_usuarios, chart_salones,
    obtener_datos_reservaciones, obtener_datos_usuarios, obtener_datos_salones
)

# --- AJAX views ---
from .ajax_views import (
    top_calificacion, top_precio, top_ingresos,
    salon_create, salon_edit, salon_delete, salon_info,
    reservacion_create, reservacion_edit, reservacion_delete,
    crear_usuario, eliminar_usuario
)

# --- DRF ViewSets ---
from .api_views import SalonViewSet, ReservacionViewSet

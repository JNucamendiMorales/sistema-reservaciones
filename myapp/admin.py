from django.contrib import admin

# --- Override del template de login del Admin default ---
admin.site.login_template = "admin_custom/login_admin.html"

# Si luego registras modelos, van aquí:
# from .models import Salon, Reservacion
# admin.site.register(Salon)
# admin.site.register(Reservacion)

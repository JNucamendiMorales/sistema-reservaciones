"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views as reservaciones_views
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from myapp.views import pagina_inicio, SalonViewSet

from django.conf import settings
from django.conf.urls.static import static

# Redirige la raíz a /salones/
def redireccion_inicio(request):
    return redirect('lista_salones')

router = DefaultRouter()
router.register(r'salones', SalonViewSet)

urlpatterns = [
    # Raíz
    path('', pagina_inicio, name='inicio'),

    # Admin default de Django, ahora en /default_admin/
    path('default_admin/', admin.site.urls, name='default_admin'),

    # Redirige / a /salones/
    path('', redireccion_inicio),

    # Recarga automática con django-browser-reload
    path('__reload__/', include('django_browser_reload.urls')),

    # Incluye rutas definidas en myapp/urls.py
    path('', include('myapp.urls')),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='theme/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="inicio"), name='logout'),
    path('registro/', reservaciones_views.registro, name='registro'),

    # API
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views as reservaciones_views
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from myapp.views import pagina_inicio,SalonViewSet

from django.conf import settings
from django.conf.urls.static import static


# Redirige la raíz a /salones/
def redireccion_inicio(request):
    return redirect('lista_salones')

router = DefaultRouter()
router.register(r'salones', SalonViewSet)

urlpatterns = [
    path('', pagina_inicio, name='inicio'),
    path('admin/', admin.site.urls),

    # Redirige / a /salones/
    path('', redireccion_inicio),

    #Habilita recarga automática del navegador con django-browser-reload
    path('__reload__/', include('django_browser_reload.urls')),

    # Incluye rutas definidas en myapp/urls.py
    path('', include('myapp.urls')),

    # Rutas de autenticación
    path('login/', auth_views.LoginView.as_view(template_name='theme/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="inicio"), name='logout'),
    path('registro/', reservaciones_views.registro, name='registro'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




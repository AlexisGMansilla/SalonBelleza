"""
URL configuration for Estetica project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect  # Importa redirect para redirigir directamente a login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Cajas/', include(('Cajas.urls', 'Cajas'), namespace='Cajas')),
    path('Clientes/', include(('Clientes.urls', 'Clientes'), namespace='Clientes')),
    path('Ventas/', include(('Ventas.urls', 'Ventas'), namespace='Ventas')),
    path('Login/', include(('Login.urls', 'Login'), namespace='Login')), 
    path('Productos/', include(('Productos.urls', 'Productos'), namespace='Productos')),
    path('Proveedores/', include(('Proveedores.urls', 'Proveedores'), namespace='Proveedores')),
    path('ServiciosSectores/', include(('Servicios_Sectores.urls', 'Servicios_Sectores'), namespace='Servicios_Sectores')),
    path('Turnos/', include(('Turnos.urls', 'Turnos'), namespace='Turnos')),
    path('Compras/', include(('Compras.urls', 'Compras'), namespace='Compras')),
    path('', lambda request: redirect('Login:Login')),  # Redirige la raíz al login

]

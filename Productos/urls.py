from django.urls import path
from . import views

app_name = 'Productos'  # Esto define el namespace

urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('modificar/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('ingresar/', views.productos_view, name='ingresar_producto'),
]
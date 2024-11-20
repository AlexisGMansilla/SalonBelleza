from django.urls import path
from  . import views

urlpatterns = [
    path('proveedores/', views.listar_proveedores, name='menu_proveedores'),
    path('ingresarProveedor/', views.IngresarProveedor, name='ingresar_proveedor'),
    path('modificarProveedor/<int:pk>/', views.ModificarProveedor, name='modificar_proveedor'),
    path('eliminarProveedor/<int:pk>', views.EliminarProveedor, name='eliminar_proveedor'),
    path('buscar', views.BuscarProveedor, name= 'buscar_proveedor'),
]

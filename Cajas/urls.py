from django.urls import path
from . import views

urlpatterns = [
    path('ingresarCaja/', views.IngresarCaja, name='ingresar_caja'),
    path('modificarCaja/<int:pk>/', views.ModificarCaja, name='modificar_caja'),
    path('eliminarCaja/<int:pk>', views.EliminarCaja, name='eliminar_caja')
    ]
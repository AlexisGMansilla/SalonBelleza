from django.urls import path
from . import views
urlpatterns = [ 
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('ingresarCliente/', views.IngresarCliente, name='ingresar_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),  # Asegúrate de que esta línea esté presente
]

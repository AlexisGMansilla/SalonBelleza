from django.urls import path
from . import views

urlpatterns = [
    path('ingresarServicio/', views.IngresarServicio, name='ingresar_servicio'),
    path('sectores/', views.menu_sectores, name='menu_sectores'),
    path('peluqueria/', views.menu_peluqueria, name='menu_peluqueria'),
    path('editarServicio/<int:id>/', views.editar_servicio, name='editar_servicio'),
    path('eliminarServicio/<int:id>', views.eliminar_servicio, name='eliminar_servicio'),
    path('buscar', views.buscar_servicio, name= 'buscar_servicio'),
    path('peluqueria/pdf', views.top_servicios_PDF, name='top_servicios_PDF')
]
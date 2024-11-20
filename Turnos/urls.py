from django.urls import path
from . import views

app_name = 'Turnos'

urlpatterns = [
    path('Home/', views.home_view, name='home_view'),
    path('Turnos/',views.listar_turnos_por_dia, name='listar_turnos_por_dia'),
    path('ingresarTurno/',views.IngresarTurno, name='ingresar_turno'),
    path('modificarTurno/<int:pk>/', views.ModificarTurno, name='modificar_turno'),
    path('eliminarTurno/<int:pk>/', views.EliminarTurno, name='eliminar_turno'),
    path('cambiarEstadoTurno/<int:id>/',views.CambiarEstadoTurno, name='cambiar_estado_turno'),
    path('enviarFecha/', views.EnviarFecha, name='enviar_fecha'),
    path('todosLosTurnos/', views.todos_los_turnos, name='todos_los_turnos'),
]
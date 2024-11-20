from django.urls import path
from . import views

app_name = 'Login'

urlpatterns = [
    path('', views.IniciarSesion, name='Login'),  # Vista para iniciar sesión
    path('logout/', views.CerrarSesion, name='logout'),
    path('registrar/', views.RegistrarUsuario, name='registrar_usuario'),
]

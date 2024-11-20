from django.urls import path
from . import views

app_name = 'Login'  # Define el namespace 'Login'

urlpatterns = [
    path('', views.IniciarSesion, name='Login'),  # URL de inicio de sesión
    path('registrar/', views.RegistrarUsuario, name='registrar_usuario'),
    path('logout/', views.CerrarSesion, name='logout'),
]

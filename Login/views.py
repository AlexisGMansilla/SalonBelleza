from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# def IniciarSesion(request):
#     if request.method == 'GET':
#         form = CustomLoginForm()
#         return render(request, 'login.html', {'form': form})
#     else:
#         form = CustomLoginForm(request, data=request.POST)
#         if form.is_valid():
#             usuario = form.get_user()
#             login(request, usuario)
#             return redirect('Turnos:home_view')
#         else:
#             return render(request, 'login.html', {'form': form, 'error': 'Datos incorrectos'})

def RegistrarUsuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        trabajador_form = TrabajadorForm(request.POST)

        if form.is_valid() and trabajador_form.is_valid():
            # Guarda el usuario
            user = form.save()
            
            # Crea el trabajador y lo asocia al usuario
            trabajador = trabajador_form.save(commit=False)
            trabajador.usuario = user
            trabajador.save()

            # Autentica y loguea al usuario
            login(request, user)
            return redirect('Turnos:home_view')
        else:
            print(form.errors)  # Para depurar errores de formulario
            print(trabajador_form.errors)  # Para depurar errores de formulario de trabajador
    else:
        form = UserCreationForm()
        trabajador_form = TrabajadorForm()

    return render(request, 'registrar_usuario.html', {
        'form': form,
        'trabajador_form': trabajador_form
    })
@login_required(login_url='Login:Login')
def CerrarSesion(request):
    logout(request)
    return redirect('Login:Login')  # Incluye el namespace 'Login'


def IniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        usuario = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if usuario is None:
            return render(request, 'login.html', {'form': AuthenticationForm, 'error': 'Datos incorrectos'})
        else:
            login(request, usuario)
            return redirect('Turnos:home_view')
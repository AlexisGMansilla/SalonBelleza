from django.shortcuts import render, redirect,  get_object_or_404
from .models import Caja
from .forms import CajaForm
# Create your views here.

def IngresarCaja(request):
    cajas = Caja.objects.all()
    if request.method == 'POST':
        cform = CajaForm(request.POST)
        if cform.is_valid():
            cform.save()
            return redirect('Cajas:ingresar_caja')  
    else:
        cform = CajaForm()
    return render(request, 'ingresar_caja.html', {'cform': cform, 'cajas': cajas})

def ModificarCaja(request, pk):
    caja = Caja.objects.get(pk=pk)
    if request.method == 'POST':
        cform = CajaForm(request.POST, instance=caja)
        if cform.is_valid():
            cform.save()
            return redirect('Cajas:ingresar_caja')
    else:
        cform = CajaForm(instance=caja) # Muestra el formulario con los datos actuales de la caja
    return render(request, 'modificar_caja.html', {'cform': cform})

def EliminarCaja(request, pk):
    caja = Caja.objects.get(pk=pk)
    caja.delete()
    return redirect('Cajas:ingresar_caja')  
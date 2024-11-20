from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm
from .models import Proveedor
from django.db.models import Q
from django.http import JsonResponse

def listar_proveedores(request):
    proveedores= Proveedor.objects.all()
    return render(request, 'menu_proveedores.html',{'proveedores':proveedores})

def IngresarProveedor(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        provform = ProveedorForm(request.POST)
        if provform.is_valid():
            provform.save()
            return redirect('Proveedores:menu_proveedores')  # Redirección correcta
    else:
        provform = ProveedorForm()
    
    return render(request, 'ingresar_proveedor.html', {'provform': provform, 'proveedores':proveedores})

def ModificarProveedor(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    if request.method == 'POST':
        provform = ProveedorForm(request.POST, instance=proveedor)
        if provform.is_valid():
            provform.save()
            return redirect('Proveedores:menu_proveedores')
    else:
        provform = ProveedorForm(instance=proveedor)
    return render(request, 'modificar_proveedor.html', {'provform': provform})

def EliminarProveedor(request, pk):
    if request.method == 'POST':
        try:
            proveedor = get_object_or_404(Proveedor, pk=pk)
            proveedor.delete()
            return JsonResponse({'success': True, 'message': f'Proveedor {proveedor.nombreProv} eliminado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

def BuscarProveedor(request):
    buscar = request.GET.get('buscar', '')  # Obtener el valor de la búsqueda
    if buscar:
        # Filtrar proveedores por nombre o id (con .icontains para búsqueda insensible a mayúsculas/minúsculas)
        proveedores = Proveedor.objects.filter(
            Q(nombreProv__icontains=buscar) | Q(id__icontains=buscar)
        )

    return render(request, 'menu_proveedores.html', {'provform': ProveedorForm(),'proveedores':proveedores, 'buscar':buscar})

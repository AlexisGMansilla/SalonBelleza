from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from django.db.models import Q
from django.http import JsonResponse

def IngresarCliente(request):
    if request.method == 'POST':
        cliform = ClienteForm(request.POST)
        if cliform.is_valid():
            cliform.save()
            return redirect('Clientes:listar_clientes')  # Redirección correcta
    else:
        cliform = ClienteForm()

    return render(request, 'ingresar_cliente.html', {'cliform': cliform})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('Clientes:listar_clientes')
  # Redirección a la lista de clientes después de la edición
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    if request.method == 'POST':
        try:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            cliente.delete()
            return JsonResponse({'success': True, 'message': f'Cliente {cliente.nombreCli} eliminado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

def listar_clientes(request):
 # Búsqueda de clientes
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(
            Q(id__icontains=query) | Q(nombreCli__icontains=query) | Q(apellidoCli__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()    
    return render(request, 'menu_cliente.html', {'clientes': clientes, 'query': query})

def client_count(request):
    return {
        'client_count': Cliente.objects.count()
    }
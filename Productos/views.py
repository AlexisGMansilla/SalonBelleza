from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.db.models import Q, F
from datetime import date, timedelta
from django.http import JsonResponse

def listar_productos(request):
    query = request.GET.get('search', '')
    if query:
        productos = Producto.objects.filter(Q(id__icontains=query) | Q(nombreProd__icontains=query))    
    else:
        productos = Producto.objects.all()
    return render(request, 'menu_productos.html', {'productos': productos})

def productos_view(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Productos:listar_productos")  # Incluir el namespace
        else:
            print("Errores del formulario:", form.errors)  # Ver errores específicos

    else:
        form = ProductoForm()
    
    # Buscar producto por ID o nombre
    query = request.GET.get("search")
    if query:
        productos = Producto.objects.filter(Q(id__icontains=query) | Q(nombreProd__icontains=query))
        return render(request, 'menu_productos.html', {'productos': productos}) 
    else:
        productos = Producto.objects.all()

    # Renderizamos la plantilla `ingresar_producto.html`
    return render(request, "ingresar_producto.html", {"form": form, "productos": productos})

# Vista para modificar producto
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Convertimos los valores a string explícitamente
    precioUniVentaProd = f"{producto.precioUniVentaProd:.2f}"
    precioUniCompraProd = f"{producto.precioUniCompraProd:.2f}"


    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("Productos:listar_productos")
    else:
        form = ProductoForm(instance=producto)  # Pasa el producto existente al formulario

    return render(request, "modificar_producto.html", {
        "form": form,
        "producto": producto,
        "precioUniVentaProd": precioUniVentaProd,
        "precioUniCompraProd": precioUniCompraProd,
    })


# Vista para eliminar producto
def eliminar_producto(request, id):
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id=id)
            producto.delete()
            return JsonResponse({'success': True, 'message': f'Producto {producto.nombreProd} eliminado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


def productos_faltantes_y_proximos(request):
    # Productos faltantes, ordenados por la diferencia entre cantidad mínima y actual
    productos_faltantes = Producto.objects.filter(
        cantidadStockProd__lte=F('cantidadMinStockProd')
    ).annotate(
        faltante=F('cantidadMinStockProd') - F('cantidadStockProd')
    ).order_by('-faltante')  # Ordenar de mayor a menor diferencia
    
    proximos_a_vencer = Producto.objects.filter(
        fechaVencProd__lte=date.today() + timedelta(days=7)
    ).order_by('fechaVencProd')  # Ordenar por fecha de vencimiento de manera ascendente


    context = {
        'productos_faltantes': productos_faltantes,
        'proximos_a_vencer': proximos_a_vencer,
    }
    return context

def productos_count(request):
    return {
        'productos_count': Producto.objects.count()
    }
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import Servicio, Sector # Importa los modelos
from .forms import ServicioForm
from django.db.models import Q
from Turnos.models import ServicioxTurno  # Importamos ServicioxTurno para el análisis de los más solicitados
from django.db.models import Count
from django.http import JsonResponse
# pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def menu_peluqueria(request):
    servicios= Servicio.objects.all()
    servicios_mas_solicitados = ServicioxTurno.objects.values('idServicio__nombreServicio') \
                        .annotate(total_turnos=Count('idTurno')) \
                        .order_by('-total_turnos')[:5]  # Los 5 más solicitados
    return render(request, 'menu_peluqueria.html',{'servicios':servicios, 'servicios_mas_solicitados': servicios_mas_solicitados})


def menu_sectores(request):
    sectores = Sector.objects.all()
    return render(request, 'menu_sectores.html', {'sectores': sectores})

def IngresarServicio(request):
    if request.method == 'POST':
        sform = ServicioForm(request.POST)
        if sform.is_valid():
            sform.save()
            return redirect('Servicios_Sectores:menu_peluqueria')  # Redirigir a la misma página
    else:
        sform = ServicioForm()

    # Renderizar la plantilla con el formulario
    return render(request, 'ingresar_servicio.html', {'sform': sform})


def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    
    if request.method == 'POST':
        sform = ServicioForm(request.POST, instance=servicio)
        if sform.is_valid():
            sform.save()
            return redirect('Servicios_Sectores:menu_peluqueria')
    else:
        sform = ServicioForm(instance=servicio)  

    return render(request, 'editar_servicio.html', {'sform': sform})  

def eliminar_servicio(request, id):
    if request.method == 'POST':
        try:
            servicio = get_object_or_404(Servicio, id=id)
            servicio.delete()
            return JsonResponse({'success': True, 'message': f'Servicio {servicio.nombreServicio} eliminado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


def buscar_servicio(request):
    buscar = request.GET.get('buscar', '')  # Obtener el valor de la búsqueda
    if buscar:
        # Filtrar proveedores por nombre o id (con .icontains para búsqueda insensible a mayúsculas/minúsculas)
        servicios = Servicio.objects.filter(
            Q(nombreServicio__icontains=buscar) | Q(id__icontains=buscar)
        )

    return render(request, 'menu_peluqueria.html', {'sform': ServicioForm(),'servicios':servicios, 'buscar':buscar})

def top_servicios_PDF(request):
    servicios_mas_solicitados = ServicioxTurno.objects.values('idServicio__nombreServicio') \
        .annotate(total_turnos=Count('idTurno')) \
        .order_by('-total_turnos')[:5]  # Los 5 más solicitados

    template = get_template('top_servicios_PDF.html')
    context = {
        'nombre': 'Estrella Estilistas',
        'direccion': 'Caseros 681, Salta Capital',
        'correo': 'estrellaestilistas@gmail.com',
        'telefono': '3875291798',
        'servicios': servicios_mas_solicitados
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="topServicios.pdf"'

    # Generar el PDF
    result = pisa.CreatePDF(html, dest=response)
    if result.err:
        return HttpResponse('Hubo un error al generar el PDF: %s' % result.err, status=500)
    return response


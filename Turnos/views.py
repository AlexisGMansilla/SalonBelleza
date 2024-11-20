from django.shortcuts import render, redirect,  get_object_or_404
from Login.models import Trabajador
from .forms import TurnoForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, make_aware,is_aware
from django.core.exceptions import ValidationError
from datetime import timedelta, date, datetime, time
from django.utils import timezone
from collections import defaultdict
from .models import Turno , Servicio
from django.http import JsonResponse
from django.contrib import messages
from Productos.views import productos_faltantes_y_proximos
from django.db.models import Count
from Clientes.views import client_count
from Productos.views import productos_count
from django.utils.translation import gettext as _
from urllib.parse import quote

@login_required(login_url='Login:Login')
def home_view(request):
    trabajador = Trabajador.objects.get(usuario=request.user)  # Obtener el trabajador del usuario actual
    clientes_count = client_count(request)['client_count'] 
    productos_context = productos_faltantes_y_proximos(request)
    demanda_semanal = obtener_demanda_semanal()
    contadores_turnos = obtener_contadores_turnos(trabajador)  # Pasar el trabajador como argumento
    total_productos = productos_count(request)['productos_count'] 

    context = {
        'client_count': clientes_count,
        'productos_faltantes': productos_context.get('productos_faltantes', []),
        'proximos_a_vencer': productos_context.get('proximos_a_vencer', []),
        'demanda_semanal': demanda_semanal,
        'turnos_confirmados': contadores_turnos['turnos_confirmados'],
        'turnos_pendientes': contadores_turnos['turnos_pendientes'],
        'total_productos': total_productos,
    }

    return render(request, 'home.html', context)


@login_required(login_url='Login:Login')
def IngresarTurno(request):
    fecha_turno = None  # Inicializa fecha_turno al inicio
    if request.method == 'POST':
        fecha_turno = request.POST.get('fechaTurno')
        # Asegúrate de que la fecha se convierta a un objeto de fecha
        if fecha_turno:
            fecha_turno = datetime.strptime(fecha_turno, '%Y-%m-%d').date()  # Cambia el formato según sea necesario
        tform = TurnoForm(request.POST, fecha_turno=fecha_turno)
        if tform.is_valid():
            try:
                turno = tform.save(commit=False)  # No guarda aún en la base de datos
                trabajador = Trabajador.objects.get(usuario=request.user)  # Obtiene el trabajador logueado
                turno.legajoTrabajador = trabajador  # Asigna el trabajador al turno
                validar_horario_turno(tform, trabajador)
                turno.fechaTurno = fecha_turno
                turno.save()
                tform.save_m2m() # # Guarda las relaciones ManyToMany, es decir, los servicios
                return redirect('Turnos:listar_turnos_por_dia')  # Redirige a la lista de turnos
            
            except ValidationError as e:
                # Agregar el mensaje de error al formulario
                tform.add_error(None, e.message)
    else:
        tform = TurnoForm(initial={'fechaTurno': fecha_turno}, fecha_turno=fecha_turno)

    return render(request, 'ingresar_turno.html', {'tform': tform})

@login_required(login_url='Login:Login')
def ModificarTurno(request, pk):
    turno = Turno.objects.get(pk=pk)
    page_number = request.POST.get('page') if request.method == 'POST' else request.GET.get('page')

   # Verificar si el turno está cancelado
    if turno.estadoTurno == 'CANCELADO':
        messages.error(request, "No puedes modificar un turno que está cancelado.")
        return redirect(f'/Turnos/?page={page_number}')  # Redirigir después del error

    # Combina la fecha y hora del turno para obtener un datetime completo
    hora_inicio_turno = datetime.combine(turno.fechaTurno, turno.horaTurno)

    # Verifica si hora_inicio_turno ya tiene zona horaria y la añade si no la tiene
    if not is_aware(hora_inicio_turno):
        hora_inicio_turno = make_aware(hora_inicio_turno)

    # Calcula el límite para modificar el turno (una hora después de su inicio)
    hora_limite = hora_inicio_turno + timedelta(hours=1)

    # Combina fecha y hora en un solo datetime
    fecha_y_hora_actual = timezone.now()
    if fecha_y_hora_actual > hora_limite:
        messages.error(request, "No puedes modificar un turno que ha comenzado hace más de una hora.")
        return redirect(f'/Turnos/?page={page_number}')  # Redirigir después del error

    if request.method == 'POST':
        tform = TurnoForm(request.POST, instance=turno)  # Crea el formulario con la instancia del turno existente
        if tform.is_valid():
            try:
                # Valida el horario del turno
                trabajador = Trabajador.objects.get(usuario=request.user)  # Obtiene el trabajador logueado
                validar_horario_turno(tform, trabajador, turno)  # Valida los horarios

                tform.save()  # Guarda el turno
                return redirect(f'/Turnos/?page={page_number}')  # Redirige a la semana donde estaba el turno
            
            except ValidationError as e:
                # Agregar el mensaje de error al formulario
                tform.add_error(None, e.message)  # Agrega error general al formulario
        else:
            # Si el formulario no es válido, puedes manejar errores aquí si necesitas un mensaje específico
            pass  
    else:
        # Si es una solicitud GET, inicializa el formulario con los datos del turno
        tform = TurnoForm(instance=turno, initial={'horaTurno': turno.horaTurno.strftime('%H:%M')})

    return render(request, 'modificar_turno.html', {'tform': tform, 'page_number': page_number})

@login_required(login_url='Login:Login')
def EliminarTurno(request, pk):
    if request.method == 'POST':
        try:
            turno = get_object_or_404(Turno, pk=pk)
            turno.delete()
            return JsonResponse({'success': True, 'message': f'Turno eliminado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


def CambiarEstadoTurno(request, id):
    turno = get_object_or_404(Turno, id=id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        page = request.POST.get('page')  # Número de página para la redirección
        day = request.POST.get('day')  # Día específico para redirección en la pestaña

        # Verificar si el estado actual es "CONFIRMADO" o "CANCELADO" y si han pasado más de 30 minutos
        if turno.estadoTurno in ['CONFIRMADO', 'CANCELADO']:
            hora_turno = datetime.combine(turno.fechaTurno, turno.horaTurno)
            hora_turno_aware = timezone.make_aware(hora_turno, timezone.get_current_timezone())
            tiempo_limite = hora_turno_aware + timedelta(minutes=30)

            if timezone.now() > tiempo_limite:
                messages.error(request, 'No puedes cambiar el estado de un turno confirmado o cancelado después de 30 minutos de su horario asignado.')
                return redirect(f'/Turnos/?page={page}&day={day}')

        # Verificar que el nuevo estado esté entre los permitidos
        if nuevo_estado in ['PENDIENTE', 'CONFIRMADO', 'CANCELADO']:
            turno.estadoTurno = nuevo_estado
            turno.save()
            messages.success(request, 'Estado del turno actualizado exitosamente.')
            return redirect(f'/Turnos/?page={page}&day={day}')
        else:
            messages.error(request, 'Estado no permitido.')

    return redirect(f'/Turnos/?page={page}&day={day}')

def listar_turnos_por_dia(request):
    trabajador = Trabajador.objects.get(usuario=request.user)
    turnos = Turno.objects.filter(legajoTrabajador=trabajador).order_by('fechaTurno', 'horaTurno')

    # Obtiene la semana actual según el número de página
    page_number = int(request.GET.get('page', 0))
    fecha_actual = date.today()
    fecha_central = fecha_actual + timedelta(weeks=page_number)
    fecha_inicio = fecha_central - timedelta(days=fecha_central.weekday())  # Lunes de la semana actual
    fecha_fin = fecha_inicio + timedelta(days=6)  # Domingo de la semana actual
    rango_semana = f"{fecha_inicio.strftime('%d-%m')} al {fecha_fin.strftime('%d-%m')}"

    # Contadores por semana
    turnos_confirmados_count = turnos.filter(
        estadoTurno='CONFIRMADO',
        fechaTurno__range=[fecha_inicio, fecha_fin]
    ).count()
    turnos_pendientes_count = turnos.filter(
        estadoTurno='PENDIENTE',
        fechaTurno__range=[fecha_inicio, fecha_fin]
    ).count()
    turnos_cancelados_count = turnos.filter(
        estadoTurno='CANCELADO',
        fechaTurno__range=[fecha_inicio, fecha_fin]
    ).count()

    # Agrupación de turnos por día en la semana actual
    days = defaultdict(lambda: {'name': '', 'date': '', 'turnos': []})
    for turno in turnos:
        day_key = turno.fechaTurno
        if fecha_inicio <= day_key <= fecha_fin:
            if day_key not in days:
                days[day_key]['name'] = _(day_key.strftime('%A'))
                days[day_key]['date'] = day_key.strftime('%d-%m')
            # Generar enlace de WhatsApp
            enlace_whatsapp = generar_enlace_whatsapp(turno.idCliente, turno.fechaTurno, turno.horaTurno)
            turno.enlace_whatsapp = enlace_whatsapp
            days[day_key]['turnos'].append(turno)

    days_list = [{'name': day['name'], 'date': day['date'], 'turnos': day['turnos']} for day in days.values()]
    days_list.sort(key=lambda x: x['date'])

    return render(request, 'listar_turnos.html', {
        'days': days_list,
        'rango_semana': rango_semana,  # Nuevo rango de semana
        'fecha_actual': fecha_actual,
        'page_number': page_number,
        'turnos_pendientes_count': turnos_pendientes_count,
        'turnos_confirmados_count': turnos_confirmados_count,
        'turnos_cancelados_count': turnos_cancelados_count
    })



def validar_horario_turno(tform, trabajador, turno_modificado=None):
    # Definición de horarios laborales
    inicio_morning = time(8, 0, 0)  # 08:00 AM
    fin_morning = time(12, 0, 0)    # 12:00 PM
    inicio_afternoon = time(14, 0, 0)  # 02:00 PM
    fin_afternoon = time(21, 0, 0)   # 09:00 PM

    # Obtener la duración total de los servicios seleccionados
    servicios_ids = tform.cleaned_data.get('servicios')
    duracion_total = sum(Servicio.objects.get(nombreServicio=servicio_id).duracion for servicio_id in servicios_ids)

    # Crear el objeto turno sin guardar aún
    turno = tform.save(commit=False)
    
    # Calcular la hora de inicio y de fin del nuevo turno
    hora_inicio_turno = datetime.combine(turno.fechaTurno, turno.horaTurno)
    hora_fin_turno = hora_inicio_turno + timedelta(minutes=duracion_total)

    # Verificar si el turno está en el pasado
    if turno.fechaTurno < date.today() or (turno.fechaTurno == date.today() and turno.horaTurno < datetime.now().time()):
        raise ValidationError("No puedes agendar un turno para una hora pasada.")

    # Definir los límites de horario laboral para el día del turno
    inicio_morning = datetime.combine(turno.fechaTurno, inicio_morning)
    fin_morning = datetime.combine(turno.fechaTurno, fin_morning)
    inicio_afternoon = datetime.combine(turno.fechaTurno, inicio_afternoon)
    fin_afternoon = datetime.combine(turno.fechaTurno, fin_afternoon)

    # Verificar si el turno está dentro del horario laboral
    if not (
        (hora_inicio_turno >= inicio_morning and hora_fin_turno <= fin_morning) or
        (hora_inicio_turno >= inicio_afternoon and hora_fin_turno <= fin_afternoon)
    ):
        raise ValidationError("El turno está fuera del horario laboral de la estética (08:00 a 12:00 y 14:00 a 21:00).")

    # Obtener los turnos existentes del trabajador para esa fecha, excluyendo cancelados
    turnos_existentes = Turno.objects.filter(
        legajoTrabajador=trabajador, 
        fechaTurno=turno.fechaTurno
    ).exclude(
        estadoTurno='CANCELADO'
    )

    # Excluir el turno que se está modificando (en caso de ser una modificación)
    if turno_modificado:
        turnos_existentes = turnos_existentes.exclude(pk=turno_modificado.pk)

    # Verificar superposición de horarios
    for t_existente in turnos_existentes:
        # Calcular hora de inicio y fin del turno existente
        duracion_existente = sum(servicio.duracion for servicio in t_existente.servicios.all())
        hora_inicio_existente = datetime.combine(t_existente.fechaTurno, t_existente.horaTurno)
        hora_fin_existente = hora_inicio_existente + timedelta(minutes=duracion_existente)

        # Condición de solapamiento
        if (hora_inicio_turno < hora_fin_existente and hora_fin_turno > hora_inicio_existente):
            raise ValidationError(f"Ya existe un turno en este horario desde {hora_inicio_existente.time()} hasta {hora_fin_existente.time()}.")

    print("Validación de horario completada exitosamente.")


def EnviarFecha(request):
    if request.method == 'POST':
        fecha_turno = request.POST.get('fechaTurno')
        print(f'La fecha es {fecha_turno} - Tiempo de solicitud: {datetime.now()}')
        # Convierte la fecha a objeto datetime (asumiendo que la fecha llega en formato 'YYYY-MM-DD')
        fecha_turno_dt = datetime.strptime(fecha_turno, '%Y-%m-%d').date()
        # Crea una instancia de tu formulario
        formulario = TurnoForm()

        # Llama a la función generar_opciones_hora con la fecha recibida
        opciones_horas = formulario.generar_opciones_hora(fecha_turno_dt)

        return JsonResponse({'opciones_horas': opciones_horas})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

# obtener demanda semanal para grafico
def obtener_demanda_semanal():
    """Obtiene la demanda semanal de turnos confirmados agrupados por día, excluyendo domingo."""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Lunes
    end_of_week = start_of_week + timedelta(days=5)  # Sábado (excluir domingo)

    # Consulta los turnos confirmados de lunes a sábado
    turnos_por_dia = Turno.objects.filter(
        estadoTurno='CONFIRMADO',
        fechaTurno__range=[start_of_week, end_of_week]
    ).values('fechaTurno').annotate(count=Count('id'))

    # Inicializa los días de la semana con 0 turnos (lunes a sábado)
    demanda_semanal = {start_of_week + timedelta(days=i): 0 for i in range(6)}
    for turno in turnos_por_dia:
        demanda_semanal[turno['fechaTurno']] = turno['count']

    return list(demanda_semanal.values())


def obtener_contexto_productos(request):
    # """Obtiene el contexto de productos faltantes y próximos a vencer."""
    return productos_faltantes_y_proximos(request)


def obtener_contadores_turnos(trabajador, page_number=0):
    # Calcula el rango de fechas para la semana actual según el número de página
    today = now().date()
    fecha_central = today + timedelta(weeks=page_number)
    fecha_inicio = fecha_central - timedelta(days=fecha_central.weekday())  # Lunes
    fecha_fin = fecha_inicio + timedelta(days=6)  # Domingo

    # Filtra los turnos del trabajador en la semana actual
    turnos_confirmados = Turno.objects.filter(
        estadoTurno='CONFIRMADO',
        legajoTrabajador=trabajador,
        fechaTurno__range=[fecha_inicio, fecha_fin]
    ).count()

    turnos_pendientes = Turno.objects.filter(
        estadoTurno='PENDIENTE',
        legajoTrabajador=trabajador,
        fechaTurno__range=[fecha_inicio, fecha_fin]
    ).count()


    return {
        'turnos_confirmados': turnos_confirmados,
        'turnos_pendientes': turnos_pendientes,
    }

def generar_enlace_whatsapp(cliente, fecha, hora):
    if not cliente.telefonoCli:
        return "#"  # Si no hay teléfono, no genera enlace
    
    # Asegurarse de que el número esté en formato internacional
    telefono = ''.join(filter(str.isdigit, str(cliente.telefonoCli)))
    
    # Mensaje con emojis
    mensaje = (
        "👋 Hola, te saludamos de ⭐Estrella Estilistas.\n"
        f"📅 Tu turno está reservado para el día {fecha.strftime('%d-%m-%Y')}\n"
        f"🕒 A las {hora.strftime('%H:%M')}.\n"
        "¡Te esperamos con mucho gusto! ✨"
    )
    
    # Codificar el mensaje correctamente
    mensaje_codificado = quote(mensaje.encode('utf-8'))
    
    # Generar enlace
    enlace = f"https://api.whatsapp.com/send?phone={telefono}&text={mensaje_codificado}&type=phone_number&app_absent=0"
    return enlace

def todos_los_turnos(request):
    # Calcular semana actual
    page_number = int(request.GET.get('page', 0))
    fecha_actual = date.today()
    fecha_central = fecha_actual + timedelta(weeks=page_number)
    inicio_semana = fecha_central - timedelta(days=fecha_central.weekday())
    fin_semana = inicio_semana + timedelta(days=6)

    # Obtener turnos ordenados por fecha y hora
    turnos = Turno.objects.filter(fechaTurno__range=[inicio_semana, fin_semana]).order_by('fechaTurno', 'horaTurno')

    contexto = {
        'turnos': turnos,
        'rango_semana': f"{inicio_semana.strftime('%d-%m')} al {fin_semana.strftime('%d-%m')}",
        'page_number': page_number,
    }
    return render(request, 'todos_los_turnos.html', contexto)

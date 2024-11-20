from django import forms
from .models import Turno
from datetime import datetime, timedelta, time, date
from Servicios_Sectores.models import Servicio
from django.core.exceptions import ValidationError

# Definición del formulario basado en el modelo Turno
class TurnoForm(forms.ModelForm):
    # Campo para seleccionar múltiples servicios
    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-multiple'}),  # Añade la clase
        required=False
    )

    # Campo para seleccionar la fecha del turno
    fechaTurno = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'id': 'id_fechaTurno'}),  # Selector de fecha HTML5
        input_formats=['%Y-%m-%d']  # Formato de fecha que acepta el campo
    )

    # Campo para seleccionar la hora del turno
    horaTurno = forms.ChoiceField(
        required=False,  # El campo es opcional
        widget=forms.Select(attrs={'id': 'id_horaTurno'})  # Se usa un widget desplegable para las opciones
    )

    # Configuración de los campos que se incluirán en el formulario
    class Meta:
        model = Turno  # Modelo asociado
        fields = ['idCliente', 'fechaTurno', 'horaTurno', 'servicios']  # Campos incluidos en el formulario
    
    def clean_servicios(self):
        servicios = self.cleaned_data.get('servicios')
        if len(servicios) > 3:
            raise ValidationError("No puedes seleccionar más de 3 servicios.")
        return servicios

    # Inicializador del formulario
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        # Obtén la fecha_turno desde kwargs, si se proporciona
        fecha_turno = kwargs.pop('fecha_turno', None)
        super().__init__(*args, **kwargs)

        fecha_turno = self.initial.get('fechaTurno') or fecha_turno

        # Solo generar opciones de hora si fecha_turno tiene un valor y no hay hora seleccionada
        if fecha_turno:
            self.fields['horaTurno'].choices = self.generar_opciones_hora(fecha_turno)
        else:
            self.fields['horaTurno'].choices = self.generar_opciones_hora(date.today())

        if self.instance and self.instance.pk:  # Asegúrate de que instance y pk son válidos
            # Supongamos que tienes una relación ManyToMany entre Turno y Servicio
            # y que `servicios` es el campo que contiene los servicios seleccionados en el formulario
            servicios_seleccionados = self.instance.servicios.all()  # Obtiene todos los servicios asociados al turno
            duracion_total = sum(servicio.duracion for servicio in servicios_seleccionados)  # Asumiendo que `duracion` está en minutos

            # Obtén el legajo del trabajador y la fecha del turno actual
            trabajador = self.instance.legajoTrabajador
            fecha = self.instance.fechaTurno

            # Filtra los turnos existentes para ese trabajador y fecha, excluyendo el turno que estamos modificando
            turnos_ocupados = Turno.objects.filter(
                legajoTrabajador=trabajador,
                fechaTurno=fecha
            ).exclude(
                pk=self.instance.pk
            ).exclude(
                estadoTurno='CANCELADO'
            )
            print(f'laaa {fecha}')


            # Convierte los turnos ocupados a una lista de intervalos
            intervalos_ocupados = []
            for turno in turnos_ocupados:
                # Duración de los servicios de ese turno
                duracion_turno = sum(servicio.duracion for servicio in turno.servicios.all())
                hora_inicio = datetime.combine(datetime.today(), turno.horaTurno)
                hora_fin = hora_inicio + timedelta(minutes=duracion_turno)  # Calcula la hora de fin del turno

                # Añade el intervalo ocupado (hora de inicio y hora de fin)
                intervalos_ocupados.append((hora_inicio.time(), hora_fin.time()))

            # Define todas las posibles horas en intervalos de 30 minutos (de 8:00 a 12:00 y de 14:00 a 21:00)
            HORAS_POSIBLES = [
                ('08:00', '08:00'),
                ('08:30', '08:30'),
                ('09:00', '09:00'),
                ('09:30', '09:30'),
                ('10:00', '10:00'),
                ('10:30', '10:30'),
                ('11:00', '11:00'),
                ('11:30', '11:30'),
                ('12:00', '12:00'),
                ('14:00', '14:00'),
                ('14:30', '14:30'),
                ('15:00', '15:00'),
                ('15:30', '15:30'),
                ('16:00', '16:00'),
                ('16:30', '16:30'),
                ('17:00', '17:00'),
                ('17:30', '17:30'),
                ('18:00', '18:00'),
                ('18:30', '18:30'),
                ('19:00', '19:00'),
                ('19:30', '19:30'),
                ('20:00', '20:00'),
                ('20:30', '20:30'),
                ('21:00', '21:00')
            ]

            # Filtra las horas para eliminar las ocupadas
            horas_disponibles = []
            for hora in HORAS_POSIBLES:
                hora_inicial = datetime.strptime(hora[0], '%H:%M').time()
                fin_hora_inicial = (datetime.combine(datetime.today(), hora_inicial) + timedelta(minutes=duracion_total)).time()
                
                # Verifica si el intervalo está ocupado
                if not any(inicio <= hora_inicial < fin for inicio, fin in intervalos_ocupados):
                    horas_disponibles.append(hora)

            # Asigna las horas disponibles al campo 'horaTurno'
            self.fields['horaTurno'].choices = horas_disponibles


    

    # Método para generar las horas disponibles para un turno en una fecha específica
    def generar_opciones_hora(self, fecha_turno):
        opciones = []
        inicio_morning = time(8, 0)  # Inicio de la mañana
        fin_morning = time(12, 0)    # Fin de la mañana
        inicio_afternoon = time(14, 0)  # Inicio de la tarde
        fin_afternoon = time(21, 0)     # Fin de la tarde

        print(f'Laaa fecha es {fecha_turno}')
        # Obtener los turnos existentes en esa fecha, excluyendo el actual si es edición y excluyendo los cancelados
        turnos_existentes = Turno.objects.filter(
            fechaTurno=fecha_turno
        ).exclude(
            pk=self.instance.pk if self.instance else None
        ).exclude(
            estadoTurno='CANCELADO'  # Excluye los turnos con estado "CANCELADO"
        )

        # Conjunto para almacenar horas ocupadas
        horas_ocupadas = set()

        # Iteramos sobre los turnos existentes en esa fecha
        for turno in turnos_existentes:
            # Verificamos si los servicios asociados al turno tienen duración
            duracion_turno = timedelta(minutes=sum(servicio.duracion for servicio in turno.servicios.all()))
            inicio_turno = datetime.combine(turno.fechaTurno, turno.horaTurno)  # Hora inicio del turno
            fin_turno = inicio_turno + duracion_turno  # Calcula la hora fin del turno

            print(f"Turno existente: {inicio_turno} a {fin_turno} (Duración: {duracion_turno})")  # Depuración

            # Agrega cada intervalo de 30 minutos entre el inicio y el fin del turno a las horas ocupadas
            hora_actual = inicio_turno
            while hora_actual < fin_turno:
                horas_ocupadas.add(hora_actual.time())  # Guarda la hora ocupada
                hora_actual += timedelta(minutes=30)

        print(f"Horas ocupadas: {horas_ocupadas}")  # Verificación

        # Generar las opciones de la mañana
        hora_actual = inicio_morning
        while hora_actual < fin_morning:
            if hora_actual not in horas_ocupadas or (self.instance and hora_actual == self.instance.horaTurno):
                opciones.append((hora_actual.strftime('%H:%M'), hora_actual.strftime('%H:%M')))
            hora_actual = (datetime.combine(fecha_turno, hora_actual) + timedelta(minutes=30)).time()

        # Generar las opciones de la tarde
        hora_actual = inicio_afternoon
        while hora_actual < fin_afternoon:
            if hora_actual not in horas_ocupadas or (self.instance and hora_actual == self.instance.horaTurno):
                opciones.append((hora_actual.strftime('%H:%M'), hora_actual.strftime('%H:%M')))
            hora_actual = (datetime.combine(fecha_turno, hora_actual) + timedelta(minutes=30)).time()
        print(f"Opciones generadas: {opciones}")  # Depuración para verificar las horas generadas

        return opciones

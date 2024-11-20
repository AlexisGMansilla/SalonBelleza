from .models import Trabajador
from datetime import datetime

dias_semana = {
    'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
    'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}

meses_anio = {
    'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
    'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
    'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
}

def trabajador_context(request):
    if request.user.is_authenticated:
        try:
            trabajador = Trabajador.objects.get(usuario=request.user)
            # Obtén la fecha actual
            fecha_actual = datetime.now()
            dia = dias_semana[fecha_actual.strftime('%A')]
            mes = meses_anio[fecha_actual.strftime('%B')]
            # Formato: Miércoles, 30 Octubre 2024
            fecha_formateada = f"{dia}, {fecha_actual.day} {mes} {fecha_actual.year}"
            
            return {
                'trabajador_nombre': trabajador.nombreTrab,
                'trabajador_email': trabajador.emailTrab,
                'fecha_formateada': fecha_formateada,
            }
        except Trabajador.DoesNotExist:
            return {}  # Devuelve un diccionario vacío si no se encuentra el trabajador
    return {}  # Devuelve un diccionario vacío si el usuario no está autenticado

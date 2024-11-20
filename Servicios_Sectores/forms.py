from django import forms
from .models import Servicio, ServicioxTurno


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['idSector', 'nombreServicio', 'duracion', 'precioUni']

class ServicioxTurnoForm(forms.ModelForm):

    class Meta:
        model = ServicioxTurno
        fields = ['idTurno', 'idServicio']
     

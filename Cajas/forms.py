from django import forms
from .models import Caja

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['nombreCaja', 'estadoCaja', 'montoCaja']
        widgets = {
            'abierta': forms.CheckboxInput()  # Usa un checkbox para el campo booleano
        }
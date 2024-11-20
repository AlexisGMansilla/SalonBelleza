from django import  forms
from .models import Proveedor
from django.core.exceptions import ValidationError
import re
from datetime import datetime

class ProveedorForm(forms.ModelForm):
    
    # Campo para seleccionar la fecha del turno
    fechaContratoProv = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'id': 'id_fechaTurno'}),  # Selector de fecha HTML5
        input_formats=['%Y-%m-%d']  # Formato de fecha que acepta el campo
    )

    class Meta:
        model = Proveedor
        fields = ['nombreProv', 'domicilioProv', 'telefonoProv', 'fechaContratoProv', 'emailProv']
    
    def clean_nombreProv(self):
        nombre = self.cleaned_data.get('nombreProv')
        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise ValidationError("El nombre solo debe contener letras y espacios.")
        return nombre

    def clean_domicilioProv(self):
        domicilio = self.cleaned_data.get('domicilioProv')
        # Validar que solo contenga letras, números y espacios
        if not re.match(r'^[a-zA-Z0-9\s]+$', domicilio):
            raise ValidationError("El domicilio solo debe contener letras, números y espacios.")
        return domicilio

    def clean_telefonoProv(self):
        telefono = self.cleaned_data.get('telefonoProv')
        # Validar que solo contenga números y el signo '+'
        if not re.match(r'^\+?\d+$', telefono):
            raise ValidationError("El teléfono solo debe contener números y el signo '+'.")
        return telefono

    

from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError
import re

class ClienteForm(forms.ModelForm):
    fechaNacCli = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={
                'type': 'date',
                'min': '1940-01-01'  # Restricción para fechas anteriores a 1940
            }
        ),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Cliente
        fields = ['nombreCli', 'apellidoCli', 'domicilioCli', 'telefonoCli', 'fechaNacCli', 'emailCli']

    def clean_nombreCli(self):
        nombre = self.cleaned_data.get('nombreCli')
        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise ValidationError("El nombre solo debe contener letras y espacios.")
        return nombre

    def clean_apellidoCli(self):
        apellido = self.cleaned_data.get('apellidoCli')
        # Validar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-Z\s]+$', apellido):
            raise ValidationError("El apellido solo debe contener letras y espacios.")
        return apellido

    def clean_domicilioCli(self):
        domicilio = self.cleaned_data.get('domicilioCli')
        # Validar que solo contenga letras, números y espacios
        if not re.match(r'^[a-zA-Z0-9\s]+$', domicilio):
            raise ValidationError("El domicilio solo debe contener letras, números y espacios.")
        return domicilio

    def clean_telefonoCli(self):
        telefono = self.cleaned_data.get('telefonoCli')
        # Validar que solo contenga números y el signo '+'
        if not re.match(r'^\+?\d+$', telefono):
            raise ValidationError("El teléfono solo debe contener números y el signo '+'.")
        return telefono

    def clean_fechaNacCli(self):
        fecha_nac = self.cleaned_data.get('fechaNacCli')
        # Validar que la fecha de nacimiento sea posterior a 1940
        if fecha_nac and fecha_nac.year < 1940:
            raise ValidationError("La fecha de nacimiento debe ser posterior a 1940.")
        return fecha_nac
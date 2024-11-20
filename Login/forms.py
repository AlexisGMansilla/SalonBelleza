from django import forms
from .models import (Trabajador)
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'estrella@email.com',
            'type': 'email'
        }),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
            'autocomplete': 'current-password'
        }),
        label="Contraseña"
    )
class TrabajadorForm(forms.ModelForm):

    fechaNacTrab = forms.DateField(
    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    input_formats=['%Y-%m-%d']
    )

    fechaInicioTrab = forms.DateField(
    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    input_formats=['%Y-%m-%d']
    )


    class Meta:
        model = Trabajador
        fields = [ 'cuilTrab', 'nombreTrab', 'apellidoTrab', 'domicilioTrab', 'telefonoTrab', 'fechaNacTrab', 'emailTrab', 'fechaInicioTrab']
    
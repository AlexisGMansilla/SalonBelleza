from django import forms
from .models import Producto
from datetime import date
import re

class ProductoForm(forms.ModelForm):
    fechaVencProd = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'min': date.today().isoformat()
            }
        ),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Producto
        fields = ['nombreProd', 'cantidadStockProd', 'marcaProd', 'precioUniVentaProd', 'precioUniCompraProd', 'cantidadMinStockProd', 'fechaVencProd']

    # Validación para Nombre del Producto y Marca
    def clean_nombreProd(self):
        nombreProd = self.cleaned_data.get('nombreProd')
        if not re.match(r'^[A-Za-z0-9 ]+$', nombreProd):
            raise forms.ValidationError("El campo solo debe contener letras y números.")
        return nombreProd

    def clean_marcaProd(self):
        marcaProd = self.cleaned_data.get('marcaProd')
        if not re.match(r'^[A-Za-z0-9 ]+$', marcaProd):
            raise forms.ValidationError("El campo solo debe contener letras y números.")
        return marcaProd

    # Validación para Cantidad en Stock, Precio Unitario de Venta, Precio Unitario de Compra y Cantidad Mínima en Stock
    def clean_cantidadStockProd(self):
        cantidadStockProd = self.cleaned_data.get('cantidadStockProd')
        if not str(cantidadStockProd).isdigit():
            raise forms.ValidationError("Este campo solo debe contener números.")
        return cantidadStockProd

    def clean_precioUniVentaProd(self):
        precioUniVentaProd = self.cleaned_data.get('precioUniVentaProd')
        try:
            precioUniVentaProd = float(precioUniVentaProd)  # Convertir a float
            if precioUniVentaProd <= 0:
                raise forms.ValidationError("Este campo debe ser un número positivo.")
        except (ValueError, TypeError):
            raise forms.ValidationError("Este campo solo debe contener números.")
        return precioUniVentaProd

    def clean_precioUniCompraProd(self):
        precioUniCompraProd = self.cleaned_data.get('precioUniCompraProd')
        try:
            precioUniCompraProd = float(precioUniCompraProd)  # Convertir a float
            if precioUniCompraProd <= 0:
                raise forms.ValidationError("Este campo debe ser un número positivo.")
        except (ValueError, TypeError):
            raise forms.ValidationError("Este campo solo debe contener números.")
        return precioUniCompraProd

    def clean_cantidadMinStockProd(self):
        cantidadMinStockProd = self.cleaned_data.get('cantidadMinStockProd')
        if not str(cantidadMinStockProd).isdigit():
            raise forms.ValidationError("Este campo solo debe contener números.")
        return cantidadMinStockProd

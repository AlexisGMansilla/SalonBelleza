from django import forms
from .models import Compra , CompraxProducto


class CompraForm(forms.ModelForm):

    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.SelectMultiple(),  # O SelectMultiple() si prefieres un menú desplegable
        required=False
    )

    fechaCompra = forms.DateField(
    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    input_formats=['%Y-%m-%d']
    )

    horaCompra = forms.TimeField(
    widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
    input_formats=['%H:%M']
    )

    class Meta:
        model = Compra
        fields = ['idProveedor', 'legajoTrabajador', 'fechaCompra', 'horaCompra', 'productos']
    



class CompraxProductoForm(forms.ModelForm):
    class Meta:
        model = CompraxProducto
        fields = ['idCompra', 'codigoProducto', 'cantidadProducto', 'montoTotal']
from django import  forms
from .models import Venta , Detalle_Venta
from Productos.models import Producto
from Servicios_Sectores.models import ServicioxTurno

class VentaForm(forms.ModelForm):

    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.SelectMultiple(),  # O SelectMultiple() si prefieres un menú desplegable
        required=False
    )
    
    servicios = forms.ModelMultipleChoiceField(
        queryset=ServicioxTurno.objects.all(),
        widget=forms.SelectMultiple(),  # O SelectMultiple() si prefieres un menú desplegable
        required=False
    )

    fechaVenta = forms.DateField(
    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    input_formats=['%Y-%m-%d']
    )

    horaVenta = forms.TimeField(
    widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
    input_formats=['%H:%M']
    )

    class Meta:
        model = Venta
        fields = ['idCliente', 'idCaja', 'fechaVenta', 'horaVenta','productos','servicios']
   



class Detalle_VentaForm(forms.ModelForm):
    class Meta:
        model = Detalle_Venta
        fields = ['idVenta', 'idServicioxTurno', 'codigoProducto', 'cantProducto', 'montoTotal']
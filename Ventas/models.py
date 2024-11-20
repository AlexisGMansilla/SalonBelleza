from django.db import models
from Clientes.models import Cliente
from Productos.models import Producto
from Servicios_Sectores.models import ServicioxTurno
from Cajas.models import Caja

# Create your models here.
class Venta(models.Model):
    idCliente = models.ForeignKey( Cliente , on_delete=models.CASCADE)  # Referencia de cadena
    idCaja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    fechaVenta = models.DateField()
    horaVenta = models.TimeField()
    productos = models.ManyToManyField( Producto , through='Detalle_Venta')
    servicios = models.ManyToManyField( ServicioxTurno , through='Detalle_Venta')

    def _str_(self):
        return f"Venta {self.id} - Cliente: {self.idCliente.nombreCli} - Fecha: {self.fechaVenta}"

class Detalle_Venta(models.Model):
    idVenta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    idServicioxTurno = models.ForeignKey( ServicioxTurno,on_delete=models.CASCADE)
    codigoProducto = models.ForeignKey( Producto , on_delete=models.CASCADE)
    cantProducto = models.BigIntegerField()
    montoTotal = models.FloatField()

    def _str_(self):
        return f"Detalle Venta {self.idVenta.id} - Producto: {self.codigoProducto.nombreProd} - Monto total: {self.montoTotal}"

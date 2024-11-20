from django.db import models
from Proveedores.models import Proveedor
from Productos.models import Producto
from Login.models import Trabajador

# Create your models here.
class Compra(models.Model):
    idProveedor = models.ForeignKey( Proveedor , on_delete=models.CASCADE)
    legajoTrabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fechaCompra = models.DateField()
    horaCompra = models.TimeField()
    productos = models.ManyToManyField( Producto , through='CompraxProducto')

    def _str_(self):
        return f"Compra {self.id} - Proveedor {self.idProveedor.nombreProv} - Fecha {self.fechaCompra}"

class CompraxProducto(models.Model):
    idCompra = models.ForeignKey( Compra , on_delete=models.CASCADE)
    codigoProducto = models.ForeignKey( Producto , on_delete=models.CASCADE)
    cantidadProducto = models.IntegerField()
    montoTotal = models.FloatField()

    def _str_(self):
        return f"{self.cantidadProducto} unidades de {self.codigoProducto.nombreProd} para la compra {self.idCompra.id}"
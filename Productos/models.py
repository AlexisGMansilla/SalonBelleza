from django.db import models

# Create your models here.
class Producto(models.Model):
    nombreProd = models.CharField(max_length=50)
    cantidadStockProd = models.IntegerField()
    marcaProd = models.CharField(max_length=50)
    precioUniVentaProd = models.FloatField()
    precioUniCompraProd = models.FloatField()
    cantidadMinStockProd = models.IntegerField()
    fechaVencProd = models.DateField()

    def _str_(self):
        return self.nombreProd


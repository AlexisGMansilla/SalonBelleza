from django.db import models

# Create your models here.

class Caja(models.Model):

    nombreCaja = models.CharField(max_length=50)
    estadoCaja = models.BooleanField(default=False)
    montoCaja = models.FloatField()

    def __str__(self):
        return self.nombreCaja
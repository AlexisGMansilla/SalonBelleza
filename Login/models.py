from django.db import models
from Cajas.models import Caja
from django.contrib.auth.models import User

# Create your models here.

class Trabajador(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cuilTrab = models.BigIntegerField()
    nombreTrab = models.CharField(max_length=50)
    apellidoTrab = models.CharField(max_length=50)
    domicilioTrab = models.CharField(max_length=80)
    telefonoTrab = models.CharField(max_length=20)
    fechaNacTrab = models.DateField()
    emailTrab = models.EmailField(max_length=50)
    fechaInicioTrab = models.DateField()
    fechaFinTrab = models.DateField(null=True, blank=True)
    idCaja = models.ForeignKey(Caja, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombreTrab} {self.apellidoTrab}"
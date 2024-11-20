from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombreProv = models.CharField(max_length=50)
    domicilioProv = models.CharField(max_length=80)
    telefonoProv = models.CharField(max_length=20)
    fechaContratoProv = models.DateField()
    emailProv = models.EmailField(max_length=50)

    def __str__(self):
        return self.nombreProv
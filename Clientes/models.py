from django.db import models

# Create your models here.
class Cliente(models.Model):
   
    nombreCli = models.CharField(max_length=50)
    apellidoCli = models.CharField(max_length=50)
    domicilioCli = models.CharField(max_length=80)
    telefonoCli = models.CharField(max_length=20)
    fechaNacCli = models.DateField()
    emailCli = models.EmailField(max_length=80)

    def __str__(self):
        return f"{self.nombreCli} {self.apellidoCli}"
from django.db import models

# Create your models here.
class Sector(models.Model):
    nombreSector = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreSector

class Servicio(models.Model):
    nombreServicio = models.CharField(max_length=50)
    duracion = models.IntegerField()
    precioUni = models.FloatField()
    idSector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreServicio

class ServicioxTurno(models.Model):
    idServicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    # Usar el nombre del modelo como cadena
    idTurno = models.ForeignKey('Turnos.Turno', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.idServicio.nombreServicio} para el turno {self.idTurno.id}"





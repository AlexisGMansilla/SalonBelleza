from django.db import models
from Login.models import Trabajador
from Cajas.models import Caja
from Servicios_Sectores.models import Servicio,ServicioxTurno
from Clientes.models import Cliente

class Turno(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Referencia de cadena
    legajoTrabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fechaTurno = models.DateField()
    horaTurno = models.TimeField()
    estadoTurno = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    servicios = models.ManyToManyField(Servicio, through= ServicioxTurno)

    def __str__(self):
        return f"Turno de {self.idCliente.nombreCli} con {self.legajoTrabajador.nombreTrab} el {self.fechaTurno} a las {self.horaTurno}"

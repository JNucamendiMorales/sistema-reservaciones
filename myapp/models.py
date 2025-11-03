from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


# Create your models here.
class Salon(models.Model):
    
    CATEGORIAS = [
        ('reuniones', 'Reuniones'),
        ('expos', 'Expos'),
        ('fiestas', 'Fiestas'),
    ]

    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1)
    imagen = models.ImageField(upload_to='salones/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='reuniones')
    ciudad = models.CharField(max_length=100, default="CDMX")


    def __str__(self):
        return self.nombre

class Reservacion(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    estado = models.CharField(max_length=20, default='pendiente')
    pagada = models.BooleanField(default=False)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


    class Meta:
        unique_together = ('salon', 'fecha_reserva')

    def __str__(self):
        return f"{self.usuario.username} - {self.salon.nombre} ({self.fecha_reserva})"
    


class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'salon')

    def __str__(self):
        return f"{self.usuario.username} - {self.salon.nombre}"




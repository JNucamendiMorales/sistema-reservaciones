from datetime import date
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone


#Perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)





#Fecha
def default_created_at():
    return timezone.now()

# ---------------------------
# Salones
# ---------------------------
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
    servicios_extras = models.ManyToManyField('ServicioExtra', blank=True)
    created_at = models.DateTimeField(default=default_created_at)  # <-- agregar fecha de creación

    def __str__(self):
        return self.nombre

# ---------------------------
# Servicios extra
# ---------------------------
class ServicioExtra(models.Model):
    TIPOS = [
        ('reuniones', 'Reuniones'),
        ('expos', 'Expos'),
        ('fiestas', 'Fiestas'),
    ]

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_salon = models.CharField(max_length=20, choices=TIPOS)

    # ✔ NUEVO CAMPO PARA IMÁGENES
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_salon})"


# ---------------------------
# Reservaciones
# ---------------------------
class Reservacion(models.Model):
    ESTADOS = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='confirmada')
    pagada = models.BooleanField(default=False)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Servicios extra seleccionados
    servicios_extra = models.ManyToManyField(ServicioExtra, blank=True)

    class Meta:
        unique_together = ('salon', 'fecha_reserva')

    def __str__(self):
        return f"{self.usuario.username} - {self.salon.nombre} ({self.fecha_reserva})"

    @property
    def tiempo(self):
        if self.fecha_reserva < date.today():
            return "pasada"
        return "proxima"

    @property
    def activa(self):
        return self.estado == "confirmada" and self.fecha_reserva >= date.today()

# ---------------------------
# Favoritos
# ---------------------------
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'salon')

    def __str__(self):
        return f"{self.usuario.username} - {self.salon.nombre}"

from rest_framework import serializers
from .models import Salon, Reservacion
from django.contrib.auth.models import User

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'

class ReservacionSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    salon_id = serializers.PrimaryKeyRelatedField(
        queryset=Salon.objects.all(),
        source='salon',
        write_only=True
    )
    usuario = serializers.StringRelatedField(read_only=True)  # Muestra el nombre
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='usuario',
        write_only=True
    )

    class Meta:
        model = Reservacion
        fields = [
            'id',
            'salon',
            'salon_id',
            'usuario',
            'usuario_id',
            'fecha_inicio',
            'fecha_fin',
            'estado'
        ]

#Endpoints
from myapp.models import Salon, Reservacion
from rest_framework import viewsets
from myapp.serializers import SalonSerializer, ReservacionSerializer


class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

class ReservacionViewSet(viewsets.ModelViewSet):
    queryset = Reservacion.objects.all()
    serializer_class = ReservacionSerializer
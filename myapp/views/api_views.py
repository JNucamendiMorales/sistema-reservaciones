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
    
    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Avg
from myapp.models import Salon
from myapp.serializers import SalonSerializer

@api_view(['GET'])
def search_salones(request):
    query = request.GET.get('q', '').strip().lower()

    # If no query, return empty list
    if not query:
        return Response([])

    # Average price for "barato" / "caro" logic
    avg_price = Salon.objects.all().aggregate(avg=Avg('precio'))['avg']

    # PRICE FILTERS
    if query == 'barato':
        salones = Salon.objects.filter(precio__lt=avg_price)

    elif query == 'caro':
        salones = Salon.objects.filter(precio__gt=avg_price)

    else:
        # FULL SEARCH:
        salones = Salon.objects.filter(
            Q(nombre__icontains=query) |
            Q(ciudad__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__icontains=query)  # <-- Added category search
        )

    # Return full objects (includes categoria + ciudad)
    serializer = SalonSerializer(salones, many=True)
    return Response(serializer.data)

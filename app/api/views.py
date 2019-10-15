from rest_framework.generics import ListAPIView

from app.api.serializers import ShipPositionsSerializer, ShipSerializer
from app.models import Position, Ship


class ListShipsView(ListAPIView):
    serializer_class = ShipSerializer
    queryset = Ship.objects.all()


class ListShipPositionsView(ListAPIView):
    serializer_class = ShipPositionsSerializer

    def get_queryset(self):
        return (
            Position.objects.order_by('-timestamp')
            .filter(ship__imo=self.kwargs['imo'])
            # we don't need output timestamp, it's better for performance
            # reasons.
            .values('latitude', 'longitude')
        )

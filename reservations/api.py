from rest_framework import serializers, viewsets, permissions
from .models import Branch, Table, Reservation
from django.db.models import Count


# ------- SERIALIZERS -------
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'timezone']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'branch', 'name', 'capacity', 'status']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'branch', 'table', 'party_size', 'date', 'time', 'status']


# ------- VIEWSETS -------
class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]


# ------- ANALYTICS API -------
class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        data = {
            "reservations_per_day": list(
                Reservation.objects.values("date").annotate(count=Count("id"))
            ),
            "reservations_per_branch": list(
                Reservation.objects.values("branch__name").annotate(count=Count("id"))
            ),
            "waitlist_count": Reservation.objects.filter(status="pending").count(),
            "confirmed_count": Reservation.objects.filter(status="confirmed").count(),
            "canceled_count": Reservation.objects.filter(status="cancelled").count(),
        }
        return Response(data)

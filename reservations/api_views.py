# reservations/api_views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Reservation, Branch
from .serializers import ReservationSerializer, BranchSerializer


class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class AnalyticsViewSet(viewsets.ViewSet):

    def list(self, request):
        # Reservations per day
        per_day = (
            Reservation.objects.values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # Reservations per branch
        per_branch = (
            Reservation.objects.values('branch__name')
            .annotate(count=Count('id'))
            .order_by('branch__name')
        )

        return Response({
            "per_day": list(per_day),
            "per_branch": list(per_branch),
        })

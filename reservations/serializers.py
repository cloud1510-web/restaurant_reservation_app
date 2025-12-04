# reservations/serializers.py

from rest_framework import serializers
from .models import Reservation, Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'slug', 'address']


class ReservationSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'customer',
            'branch',
            'table',
            'party_size',
            'date',
            'time',
            'status',
        ]

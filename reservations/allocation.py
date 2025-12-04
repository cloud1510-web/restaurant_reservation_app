# reservations/allocation.py
from .models import Table, Reservation
from django.db.models import Q

def find_best_table(branch, party_size, date, time):
    """
    Basic best-fit: smallest table with capacity >= party_size that is free at date/time.
    If none, returns None.
    """
    # Candidate tables that are available and capacity >= party_size
    candidates = Table.objects.filter(branch=branch, status='available', capacity__gte=party_size).order_by('capacity')
    for table in candidates:
        conflict = Reservation.objects.filter(table=table, date=date, time=time, status__in=['pending','confirmed']).exists()
        if not conflict:
            return table
    # No single table fits; optionally we might try combine tables (not implemented here)
    return None

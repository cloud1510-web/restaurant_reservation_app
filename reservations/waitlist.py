from .models import Reservation
from .allocation import find_best_table

def promote_waitlist(branch, date, time):
    pending = Reservation.objects.filter(
        branch=branch,
        date=date,
        time=time,
        status='pending'
    ).order_by('waitlist_position')

    if not pending.exists():
        return None

    res = pending.first()
    table = find_best_table(branch, res.party_size, date, time)

    if table:
        res.table = table
        res.status = 'confirmed'
        res.waitlist_position = None
        res.save()
        return res
    return None

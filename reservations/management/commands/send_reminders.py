# reservations/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from reservations.models import Reservation
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Send email reminders for tomorrow's confirmed reservations."

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now().date() + timedelta(days=1)
        reservations = Reservation.objects.filter(date=tomorrow, status='confirmed')
        self.stdout.write(f"Found {reservations.count()} reservations for {tomorrow}")
        for r in reservations:
            user_email = r.customer.user.email
            if not user_email:
                self.stdout.write(f"Skipping {r.pk}: no email")
                continue
            subject = f"Reminder: your reservation at {r.branch.name} on {r.date} at {r.time}"
            body = (
                f"Hello {r.customer.user.first_name or r.customer.user.username},\n\n"
                f"This is a reminder for your reservation at {r.branch.name} on {r.date} at {r.time}.\n"
                "If you need to change or cancel, please visit your reservations page.\n\n"
                "Thank you!"
            )
            # Use send_mail configured in settings (dev: console backend)
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
            self.stdout.write(f"Sent reminder to {user_email} for reservation {r.pk}")

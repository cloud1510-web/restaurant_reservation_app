from django.db import models

# reservations/models.py
import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

ROLE_CHOICES = (('customer','Customer'),('staff','Staff'),('manager','Manager'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Branch(models.Model):
    """A restaurant branch/location"""
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    address = models.TextField(blank=True)
    timezone = models.CharField(max_length=64, blank=True, default='UTC')

    def __str__(self):
        return self.name

class Table(models.Model):
    """
    Table in a branch. We include x,y coordinates for a floorplan UI later.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='tables')
    name = models.CharField(max_length=32)  # e.g., T1, T2, Booth A
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='available')  # available / out_of_service
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('branch', 'name')
        ordering = ['branch', 'name']

    def __str__(self):
        return f"{self.branch.name} - {self.name} ({self.capacity})"

class MenuItem(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self): 
        return f"{self.name} - {self.branch.name}"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), # placed, waiting allocation
        ('confirmed', 'Confirmed'), # allocated a table
        ('cancelled', 'Cancelled'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role':'customer'}, related_name='reservations')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, null=True, blank=True, on_delete=models.SET_NULL, related_name='reservations')
    party_size = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    waitlist_position = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['branch','date','time']),
            models.Index(fields=['customer','status']),
        ]
        # Prevent exact double-booking on same table/time
        constraints = [
            models.UniqueConstraint(fields=['table','date','time'], name='unique_table_booking')
        ]
        ordering = ['-date','time']

    def reservation_datetime(self):
        """Return timezone-aware datetime for scheduled reservation."""
        dt = datetime.datetime.combine(self.date, self.time)
        if settings.USE_TZ:
            return timezone.make_aware(dt)
        return dt

    def __str__(self):
        return f"Res#{self.pk} {self.customer.user.username} {self.date} {self.time} ({self.status})"

class WaitlistEntry(models.Model):
    """If allocation engine can't find table, we create waitlist entries."""
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='waitlist_entry')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Waitlist for Res#{self.reservation.pk}"

class AuditLog(models.Model):
    """Simple audit trail for operations."""
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    extra = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.created_at} - {self.action}"


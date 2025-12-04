from django.contrib import admin
from .models import (
    Profile, Branch, Table, MenuItem, Reservation, WaitlistEntry, AuditLog
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'address')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'capacity', 'status')
    list_filter = ('branch','status')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'price', 'available')
    list_filter = ('branch','available')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','customer','branch','table','party_size','date','time','status')
    list_filter = ('status','branch','date')

admin.site.register(WaitlistEntry)
admin.site.register(AuditLog)

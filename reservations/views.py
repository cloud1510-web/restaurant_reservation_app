import json
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.db.models import Count

from .models import Branch, Reservation, Table, MenuItem
from .forms import (
    ReservationForm,
    BranchForm,
    TableForm,
    MenuItemForm
)
from .allocation import find_best_table
from .waitlist import promote_waitlist


class HomeView(TemplateView):
    template_name = 'home.html'


class BranchListView(ListView):
    model = Branch
    template_name = 'branches.html'
    context_object_name = 'branches'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_create.html'
    success_url = reverse_lazy('my_reservations')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.customer = self.request.user.profile
        branch = form.cleaned_data['branch']
        party_size = form.cleaned_data['party_size']
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']

        table = find_best_table(branch, party_size, date, time)

        if table:
            reservation.table = table
            reservation.status = 'confirmed'
            messages.success(self.request, "Reservation confirmed! 🎉")
        else:
            reservation.status = 'pending'
            messages.warning(
                self.request,
                "No tables available at this time. You were placed on the waitlist."
            )

        reservation.save()
        return super().form_valid(form)


class MyReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'my_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(customer=self.request.user.profile)


def staff_required(user):
    
    return user.is_authenticated and user.profile.role in ['staff', 'manager']


# ----------------------
# STAFF DASHBOARD
# ----------------------

@method_decorator(user_passes_test(staff_required), name='dispatch')
class StaffDashboardView(ListView):
    model = Reservation
    template_name = 'staff_dashboard.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        qs = Reservation.objects.all().order_by('date', 'time')

        branch = self.request.GET.get('branch')
        if branch:
            qs = qs.filter(branch__id=branch)

        date = self.request.GET.get('date')
        if date:
            qs = qs.filter(date=date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.all()
        return context


# ----------------------
# BRANCH CRUD
# ----------------------
@method_decorator(user_passes_test(staff_required), name='dispatch')
class BranchListViewStaff(ListView):
    model = Branch
    template_name = 'branch_list_staff.html'
    context_object_name = 'branches'


@method_decorator(user_passes_test(staff_required), name='dispatch')
class BranchCreateView(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branch_form.html'
    success_url = reverse_lazy('branches_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branch_form.html'
    success_url = reverse_lazy('branches_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class BranchDeleteView(DeleteView):
    model = Branch
    template_name = 'branch_confirm_delete.html'
    success_url = reverse_lazy('branches_staff')


# ----------------------
# TABLE CRUD
# ----------------------

@method_decorator(user_passes_test(staff_required), name='dispatch')
class TableListViewStaff(ListView):
    model = Table
    template_name = 'table_list_staff.html'
    context_object_name = 'tables'

    def get_queryset(self):
        qs = Table.objects.all().order_by('branch', 'name')
        branch = self.request.GET.get('branch')
        if branch:
            qs = qs.filter(branch__id=branch)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.all()
        return context


@method_decorator(user_passes_test(staff_required), name='dispatch')
class TableCreateView(CreateView):
    model = Table
    form_class = TableForm
    template_name = 'table_form.html'
    success_url = reverse_lazy('tables_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class TableUpdateView(UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'table_form.html'
    success_url = reverse_lazy('tables_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class TableDeleteView(DeleteView):
    model = Table
    template_name = 'table_confirm_delete.html'
    success_url = reverse_lazy('tables_staff')


# ----------------------
# MENU CRUD
# ----------------------

@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemListViewStaff(ListView):
    model = MenuItem
    template_name = 'menu_list_staff.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        qs = MenuItem.objects.all().order_by('branch', 'name')
        branch = self.request.GET.get('branch')
        if branch:
            qs = qs.filter(branch__id=branch)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.all()
        return context


@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu_form.html'
    success_url = reverse_lazy('menu_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu_form.html'
    success_url = reverse_lazy('menu_staff')


@method_decorator(user_passes_test(staff_required), name='dispatch')
class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'menu_confirm_delete.html'
    success_url = reverse_lazy('menu_staff')


# ----------------------
# RESERVATION CANCEL
# ----------------------

@method_decorator(login_required, name='dispatch')
class ReservationCancelView(DeleteView):
    model = Reservation
    template_name = 'reservation_cancel_confirm.html'
    success_url = reverse_lazy('my_reservations')

    def delete(self, request, *args, **kwargs):
        reservation = self.get_object()
        branch = reservation.branch
        date = reservation.date
        time = reservation.time

        response = super().delete(request, *args, **kwargs)

        promote_waitlist(branch, date, time)
        return response

@method_decorator(user_passes_test(lambda u: u.is_authenticated and u.profile.role == 'manager'), name='dispatch')
class ManagerAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = "manager_analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Reservations per day
        daily = (
            Reservation.objects.values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        context['dates'] = [d['date'].strftime("%Y-%m-%d") for d in daily]
        context['daily_counts'] = [d['count'] for d in daily]

        # Reservations per branch
        branch_data = (
            Reservation.objects.values('branch__name')
            .annotate(count=Count('id'))
        )

        context['branch_names'] = [b['branch__name'] for b in branch_data]
        context['branch_counts'] = [b['count'] for b in branch_data]

        # Status overview
        context['confirmed_count'] = Reservation.objects.filter(status='confirmed').count()
        context['pending_count'] = Reservation.objects.filter(status='pending').count()
        context['cancelled_count'] = Reservation.objects.filter(status='cancelled').count()

        return context

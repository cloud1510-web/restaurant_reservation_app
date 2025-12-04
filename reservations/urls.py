# reservations/urls.py

from django.urls import path, include
from rest_framework import routers

from .views import (
    HomeView, BranchListView, ReservationCreateView, MyReservationsView,
    StaffDashboardView, BranchListViewStaff, BranchCreateView, BranchUpdateView,
    BranchDeleteView, TableListViewStaff, TableCreateView, TableUpdateView,
    TableDeleteView, MenuItemListViewStaff, MenuItemCreateView,
    MenuItemUpdateView, MenuItemDeleteView, ReservationCancelView,
    ManagerAnalyticsView
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .api_views import ReservationViewSet, AnalyticsViewSet

router = routers.DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('branches/', BranchListView.as_view(), name='branches'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/my/', MyReservationsView.as_view(), name='my_reservations'),
    path('reservations/<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation_cancel'),

    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),

    # Staff CRUD
    path('staff/branches/', BranchListViewStaff.as_view(), name='branches_staff'),
    path('staff/branches/create/', BranchCreateView.as_view(), name='branch_create'),
    path('staff/branches/<int:pk>/edit/', BranchUpdateView.as_view(), name='branch_update'),
    path('staff/branches/<int:pk>/delete/', BranchDeleteView.as_view(), name='branch_delete'),

    path('staff/tables/', TableListViewStaff.as_view(), name='tables_staff'),
    path('staff/tables/create/', TableCreateView.as_view(), name='table_create'),
    path('staff/tables/<int:pk>/edit/', TableUpdateView.as_view(), name='table_update'),
    path('staff/tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),

    path('staff/menu/', MenuItemListViewStaff.as_view(), name='menu_staff'),
    path('staff/menu/create/', MenuItemCreateView.as_view(), name='menu_create'),
    path('staff/menu/<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menu_update'),
    path('staff/menu/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu_delete'),

    path('manager/analytics/', ManagerAnalyticsView.as_view(), name='manager_analytics'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # API
    path('api/v1/', include(router.urls)),

]

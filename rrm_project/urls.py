from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # ADD THIS LINE ↓↓↓
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
    # other patterns...
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # keep your app urls:
    path('', include('reservations.urls')),
    # (if you want DRF browsable login for API, put it under api-auth/)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    

    path('api/', include('reservations.urls')),
]

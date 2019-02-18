"""fiubauth URL Configuration"""
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.user_home, name='home'),
    path('home/', views.user_home),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('oidc_provider.urls', namespace='oidc_provider')),
]

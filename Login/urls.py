from django.contrib import admin, auth
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# app_name = 'signin'

urlpatterns = [
    path('', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('logout/', views.user_logout, name="logout"),
    path('edit_profile/', views.EditProfile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
    #path('.*/', views.garbage,name='redirect'),
]

from django.contrib import admin
from django.urls import path
from GeradorProposta import views

urlpatterns = [
    path('', views.home, name='home'),
]

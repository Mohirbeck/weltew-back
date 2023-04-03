from django.urls import path

from . import views

urlpatterns = [
    path('moy-sklad/', views.moy_sklad, name='moy_sklad'),
]
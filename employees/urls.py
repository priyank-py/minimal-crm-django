from django.urls import path
from . import views

urlpatterns = [
    path('emp', views.update_profile, name='testprofile'),
]

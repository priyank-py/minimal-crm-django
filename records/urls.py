from django.urls import path
from . import views

urlpatterns = [
    # path('record', views.daily_record, name='record'),
    # path('', views.profile, name='profile'),
    path('test', views.monthly_records, name='test'),
    # path('dts', views.DTSCreate.as_view(), name='dts'),
]
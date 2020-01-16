from django.urls import path
from . import views
# from records.views import daily_record

urlpatterns = [
    path('dashboard', views.dashboard, name='dash'),
    path('', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='myprofile'),
    path('reports', views.my_reports, name='reports'),
    path('icons', views.icons, name='icons'),
    path('logout', views.logout_view, name='logout'),
    path('notifications', views.notifications, name='notifications'),
    path('seven', views.sales_last_seven_days, name='seven'),
    # path('record', daily_record, name='record'),
    path('#', views.dts, name='dts')
]

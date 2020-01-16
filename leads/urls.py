from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_leads, name='listings'),
    path('all', views.all_leads, name='all_leads'),
    path('search', views.search, name='search'),
    path('<int:id>', views.single_lead, name='single_lead'),
    path('<int:id>', views.show_quotation, name='quotation'),
    # path('generate', views.generate, name='generate')
]


  # path('<int:lead_id>', views.listing, name='listing'),

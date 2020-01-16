from django.urls import path
from . import views

urlpatterns = [
    path('invoices', views.invoices, name='invoices'),
    path('<int:id>', views.lead_invoice, name='invoice'),
    path('bill/<int:id>', views.each_bill, name='lead_bill'),
    path('quotation/<int:id>', views.quotation, name='quotation'),
    path('quotations', views.all_quotation, name='all_quotations'),
    path('invoice/<int:id>', views.invoice_to_pdf_view, name='invoice2pdf'),
    path('bill_pdf/<int:id>', views.bill_to_pdf_view, name='bill2pdf'),
    path('quotation_pdf/<int:id>', views.quotation_to_pdf_view, name='quotation2pdf'),

]
from django.contrib import admin
from .models import Invoice, Bill, InstallmentData, ClientInvoice, ClientBill, ClientInstallmentData, Quotation, QuotationRatesAndTerms
# from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, SliderNumericFilter

# Register your models here.

class InstallmentDataInline(admin.StackedInline):
    model = InstallmentData
    extra = 1
    fields = ('installment_date', 'installment_amount',)


# class BillsInline(admin.StackedInline):
#     model = Bill
#     extra = 1
#     fields = ['invoice', 'bill_date', 'payment_option', 'recieve_amount', 'credit_card_no', 'dd_no', 'cheque_no', 'cheque_status','drawn_on', 'bank_name', 'bank_branch', ('change','tens', 'twenties', 'fiftys', 'hundreds', 'two_hundreds', 'five_hundreds', 'two_thousands')]

class ClientBillsInline(admin.StackedInline):
    model = ClientBill
    extra = 1
    fields = ['invoice', 'recieve_amount', 'payment_option', 'credit_card_no', 'dd_no', 'cheque_no', 'drawn_on', 'amount_in_word']



class ClientInstallmentDataInline(admin.StackedInline):
    model = ClientInstallmentData
    extra = 1
    fields = ('installment_date', 'installment_amount', 'paid')




@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('amount_in_word',)
        

@admin.register(ClientBill)
class ClientBillAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('amount_in_word',)


class InvoiceAdmin(admin.ModelAdmin):

    list_display = [ 'invoice_number','lead', 'enquired_for', 'g_total', 'counselor']

    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('sub_total', 'gst', 'g_total')
    inlines = (InstallmentDataInline,)


@admin.register(ClientInvoice)
class ClientInvoiceAdmin(admin.ModelAdmin):
    class Meta:
        model = ClientInvoice
        fields = '__all__'
        exclude = ('sub_total', 'gst', 'g_total')

    inlines = (ClientInstallmentDataInline, ClientBillsInline,)

class QuotationRatesAndTermsInline(admin.StackedInline):
    model = QuotationRatesAndTerms
    extra = 1


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'client_name' )

    class Meta:
        model = Quotation
        fields = '__all__'
    inlines = (QuotationRatesAndTermsInline,)


# admin.site.register(Bill, BillsAdmin)
admin.site.register(Invoice, InvoiceAdmin)
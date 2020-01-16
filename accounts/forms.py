# from django import forms
# from .models import Invoice, Bill
# from django.forms.models import inlineformset_factory
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, HTML, ButtonHolder, Submit
# from .custom_layout_object import Formset

# class BillForm(forms.ModelForm):
#     class Meta:
#         model = Bill
#         # fields = '__all__'
#         exclude = ()

# BillFormSet = inlineformset_factory(
#     Invoice, Bill, form=BillForm,
# fields='__all__', extra=1, can_delete=True
# )

# class InvoiceForm(forms.ModelForm):

#     class Meta:
#         model = Invoice
#         exclude = ['employee', ]

#     def __init__(self, *args, **kwargs):
#         super(DTSForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = True

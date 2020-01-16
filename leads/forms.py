# from django import forms
# from django.forms import modelformset_factory, formset_factory
# from .models import Lead



# class LeadForm(forms.ModelForm):

#     class meta:
#         model = Lead
#         fields = ('remarks', )

#         labels = {
#             'remarks': 'remarks'
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter remarks here'
#                 }
#             )
#         }

    
# RemarksModelFormset = modelformset_factory(
#     Lead,
#     fields=('remarks', ),
#     extra=1,
#     widgets={'remarks': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter remarks'
#         })
#     }
# )
    
    
from django import forms
from datetime import date
from .models import *
# from django.forms.models import inlineformset_factory
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, HTML, ButtonHolder, Submit
# from .custom_layout_object import Formset


class EmpRecordForm(forms.ModelForm):
    def clean(self):
        self.instance.submitted_on = date.today()
        return super(EmpRecordForm, self).clean()

    class Meta:
        model = EmpRecord
        fields = '__all__'
        exclude = ('submitted_on',)


# class DTSTitleForm(forms.ModelForm):
    
#     class Meta:
#         model = TargetData
#         # fields = ("",)
#         exclude = ()

# DTSFormSet = inlineformset_factory(
#     DTS, TargetData, form=DTSTitleForm,
# fields='__all__', extra=1, can_delete=True
# )

# class DTSForm(forms.ModelForm):

#     class Meta:
#         model = DTS
#         exclude = ['employee', ]

#     def __init__(self, *args, **kwargs):
#         super(DTSForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = True
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'col-md-3 create-label'
#         self.helper.field_class = 'col-md-9'
#         self.helper.layout = Layout(
#             Div(
#                 Field('employee'),
#                 Field('dated'),
#                 Fieldset('Add task', Formset('task')),
#                 ButtonHolder(Submit('submit', 'Save')),
#                 )
#             )
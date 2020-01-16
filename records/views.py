from django.shortcuts import render, redirect
from .forms import *
from datetime import datetime, date
import calendar
from .models import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction


# def daily_record(request):
#     if request.method == "POST":
#         form = EmpRecordForm(request.POST)
#         if form.is_valid:
#             record = form.save(commit=False)
#             record.employee = request.user
#             form.save()
#         return redirect('/')
#     else:
#         form = EmpRecordForm()
#     dt = date.today()
#     current_user = request.user
#     try:
#         targets = MonthlyTarget.objects.all().filter(position=current_user.profile.postion).filter(month=datetime.now().strftime('%B'))
    
#     except:
#         targets = MonthlyTarget.objects.none()
#     # print(target)

#     context = {'form':form, 'dt':dt, 'targets': targets}

#     return render(request, 'pages/records.html', context)

def monthly_records(request):

    current_month = int(datetime.now().strftime('%m'))
    current_year = int(datetime.now().strftime('%Y'))
    first_day, last_day = calendar.monthrange(current_year, current_month)
    start_month_date = datetime.today().replace(day=1)
    end_month_date = datetime.today().replace(day=last_day)

    emp_days = EmpRecord.objects.all().filter(submitted_on__lte=end_month_date).filter(employee=request.user)
    emp_records_each_day = [{j.field_name: j.value for j in i.custom_record.all()} for i in emp_days]

    context = {
        'emp_days': emp_days,
        'emp_records_each_day': emp_records_each_day,
    }

    return render(request, 'pages/testmonthly.html', context)






# class DTSCreate(CreateView):
#     model = DTS
#     template_name = 'pages/test.html'
#     form_class = DTSForm
#     success_url = None

#     def get_context_data(self, **kwargs):
#         data = super(DTSCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['task'] = DTSFormSet(self.request.POST)
#         else:
#             data['task'] = DTSFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()

#         tasks = context['task']
#         with transaction.atomic():
#             form.instance.employee = self.request.user.profile
#             self.object = form.save()
#             if tasks.is_valid():
#                 tasks.instance = self.object
#                 tasks.save()
#         return super(DTSCreate, self).form_valid(form)
    
#     def get_success_url(self):
#         return reverse_lazy('admin:records_dts_change', kwargs={'pk': self.object.pk})

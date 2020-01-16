from django.shortcuts import render, redirect
from .models import Employee
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm
from django.utils.translation import ugettext as _

# Create your views here.
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.employee)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.employee)
    return render(request, 'pages/testprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# def employee_of_month(request):
#     eom = Employee.objects.filter(is_eom=True)
#     return render(request, 'pages/about.html',{'eom':eom})
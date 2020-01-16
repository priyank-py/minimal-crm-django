from django.shortcuts import render, redirect, get_list_or_404
from employees.models import Employee
from leads.models import Lead, LeadRemarks
from records.models import MonthlyTarget, EmpRecord, EmpCustomRecord, MonthlyCustomTarget
# import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime, timedelta, date
import calendar
from records.models import DTS
from accounts.models import Bill

@login_required(login_url='admin:login')
def dashboard(request):

    # emps = Employee.objects.all()
    emp = request.user
    try:
        emps = emp.profile.get_descendants(include_self=False)
    except:
        emps = Employee.objects.none()
    leads = Lead.objects.all()
    # seven = Lead.objects.order_by('-registration_date').filter(~Q(registration_date=None))[:7]

    latest_lead_remark = [i.lead_remarks.last() for i in leads]
    registered_lead_ids = [i.lead.id for i in latest_lead_remark if hasattr(i, 'status') and (i.status == 'walkinreg' or i.status=='leadreg')]
    registered_lead_ids_past_seven_days = [i.lead for i in latest_lead_remark if hasattr(i, 'status') and (i.status == 'walkinreg' or i.status == 'leadreg') and i.next_follow_up_date > date.today() - timedelta(days=7)]
    past_seven_days = [calendar.day_name[(date.today() - timedelta(days=i)).weekday()] for i in range(6, -1, -1)]
    registered_each_days = [sum([i.course_fee if i.lead_remarks.last().next_follow_up_date == date.today() - timedelta(days=j) else 0 for i in registered_lead_ids_past_seven_days]) for j in range(6, -1, -1)]
    total_col = 0
    last_week = datetime.now() - timedelta(days=7)

    # weekly_data = Lead.objects.filter(id__in=registered_lead_ids).extra(select={'day': 'date(lead_remarks.last().next_follow_up_date)'}).values('day').annotate(sum=Sum('course_fee'))
    
    weekly_data = Lead.objects.filter(id__in=registered_lead_ids).filter()

    # seven_days = []
    # seven_data = []
    min_data = 0
    max_data = 1000
    # for dates in weekly_data:
    #     dates['day'] = datetime.strptime(dates['day'], '%Y-%m-%d')
    #     days = datetime.strftime(dates['day'], '%a')
    #     dates['day'] = days
    # seven_days = [i['day'] for i in weekly_data]
    # seven_data = [j['sum'] for j in weekly_data]
    
    current_month = int(datetime.now().strftime('%m'))
    current_year = int(datetime.now().strftime('%Y'))
    first_day, last_day = calendar.monthrange(current_year, current_month)
    start_month_date = datetime.today().replace(day=1)
    end_month_date = datetime.today().replace(day=last_day)

    current_month_in_word = datetime.now().strftime('%B')

    try:
        seven_days_bills = Bill.objects.all().filter(bill_date__lte=date.today()).filter(bill_date__gte=date.today() - timedelta(days=7))
    except:
        seven_days_bills = Bill.objects.none()

    seven_days = [i[:3] for i in past_seven_days]
    # seven_data = registered_each_days
    

    

    # if any(seven_days_bills):
    bill_each_day = [sum([i.recieve_amount if i.bill_date==(date.today() - timedelta(days=j)) else 0 for i in seven_days_bills ]) for j in range(6, -1, -1)]
    seven_data = bill_each_day
    # print('BILL EACH DAY',bill_each_day)

       

    

    try:
        emp_monthly_targets = MonthlyTarget.objects.all().filter(month=datetime.now().strftime('%B')).filter(position=emp.profile.postion).last()
    except:
        emp_monthly_targets = MonthlyTarget.objects.none()
        print('Targets Not Added Yet!')

    try:
        if request.user.profile:
            month_targets = MonthlyCustomTarget.objects.all().filter(monthly_target=emp_monthly_targets)
    except:
        month_targets = MonthlyCustomTarget.objects.all().filter(monthly_target__in=emp_monthly_targets)
    
    try:
        emp_monthly_records = EmpRecord.objects.all().filter(report_for=f'{current_year}-{current_month_in_word}').filter(employee=emp)
    except:
        emp_monthly_records = EmpRecord.objects.none()
        

    month_records = EmpCustomRecord.objects.all().filter(emp_record__in=emp_monthly_records)
    if len(month_records) > 7:
        month_records = month_records[:7]
    

    if len(month_records) < len(month_targets):
        t = len(month_targets) - len(month_records)
        new_month_records = [i for i in month_records]
        for i in range(t):
            new_month_records.append(EmpCustomRecord.objects.none())

    

    # target_and_record = [(i, j) for i in month_records for j in month_targets if i.field_name==j.field_name]
    
    # target_and_record = []
    # target_record = [[(i, j) for j in month_targets if set(i.field_name).issubset(j.field_name) or set(j.field_name).issubset(i.field_name)] for i in month_records]
    # records_and_targets = [tuple(i)[0] for i in target_record if i != []]
    

    def eithers_subset(s1, s2):
        if s1 and hasattr(i, 'field_name'):
            if (set(s1).issubset(s2) or set(s2).issubset(s1)):
                return True
            else:
                return False
        else:
            return False

    
    e = EmpCustomRecord.objects.none()
    # print('my empty set', dir(e))
    record_for_targets = [[(j, i) if eithers_subset(j, i) else ({'field_name': i.field_name, 'value': 0}, i) for j in new_month_records] for i in month_targets]
    
    # print('testing my queryset',record_for_targets)
    records_and_targets = [tuple(i)[0] for i in record_for_targets if i != []]
    # print('the record for target',records_and_targets)



    # target_mails_monthly = sum([i.mails for i in month_targets])
    # target_messages_monthly = sum([i.messages for i in month_targets])
    # target_calls_monthly = sum([i.calls for i in month_targets])
    # target_online_submissions_monthly = sum([i.online_submissions for i in month_targets])
    # target_follow_ups_monthly = sum([i.follow_ups for i in month_targets])
    
    # total_mails_monthly = sum([i.mails for i in emp_monthly_records])
    # total_messages_monthly = sum([i.messages for i in emp_monthly_records])
    # total_calls_monthly = sum([i.calls for i in emp_monthly_records])
    # total_online_submissions_monthly = sum([i.online_submissions for i in emp_monthly_records])
    # total_follow_ups_monthly = sum([i.follow_ups for i in emp_monthly_records])
    

    # emp_record_categories = ['mails', 'messages', 'calls', 'online_submissions', 'follow_ups']
    # emp_records_by_category = [total_mails_monthly, total_messages_monthly, total_calls_monthly, total_online_submissions_monthly, total_follow_ups_monthly]
    # emp_targets_by_category = [target_mails_monthly, target_messages_monthly, target_calls_monthly, target_online_submissions_monthly, target_follow_ups_monthly]
    
    # max_records_by_category = max(emp_records_by_category + emp_targets_by_category) + 100
    # min_records_by_category = 0
    
    # print('targets are: ', emp_targets_by_category)


    if any(seven_data):
        min_data = min(seven_data) - 1000
        max_data = max(seven_data) + 1000

    last_month = datetime.now() - timedelta(days=30)
    tech_data = Lead.objects.filter(id__in=registered_lead_ids).extra(select={'tech': 'enquired_for'}).values('tech').annotate(sum=Sum('course_fee'))
    

    min_col = 0
    max_col = 1000
    month_course = [i['tech'] for i in tech_data]
    month_course = [''.join([i[0]  for i in j.split()]) if len(j.split())>1 else j for j in month_course]
    month_collection = [j['sum'] if not j['sum'] == None else 0 for j in tech_data]
    if any(month_collection):
        min_col = min(month_collection) - 1000
        max_col = max(month_collection) + 1000
    # print(weekly_data)

    for i in leads:
        if i.course_fee:
            total_col += i.course_fee

    # follow_leads = LeadRemarks.objects.all().filter(next_follow_up_date__lte=date.today()).latest('next_follow_up_date')
    # unregistered_leads = [l.lead.id for l in follow_leads if l.status !='walkinreg' or l.status !='leadreg']
    # print(unregistered_leads)
    # follow_leads = Lead.objects.filter(id__in=unregistered_leads)

    # all_lead = Lead.objects.all()
    # latest_lead_remark = [i.lead_remarks.last() for i in all_lead]
    
    # unregistered_leads = [l.lead.id for l in follow_lead if l.status !='walkinreg' or l.status !='leadreg']
    # print(unregistered_leads)
    # follow_leads = Lead.objects.filter(id__in=unregistered_leads)

    # total_new = len(new_leads)
    try:
        morning_report = DTS.objects.all().filter(dated=date.today()).filter(employee=request.user.profile)
    except:
        morning_report = DTS.objects.none()

    leadclose = [i.lead if hasattr(i, 'status') and i.status == 'leadclose' else 0 for i in latest_lead_remark]
    leadwalkin = [i.lead if hasattr(i, 'status') and i.status == 'leadwalkin' else 0 for i in latest_lead_remark]
    leadfollowup = [i.lead if hasattr(i, 'status') and i.status == 'leadfollowup' else 0 for i in latest_lead_remark]
    leadreg = [i.lead if hasattr(i, 'status') and i.status == 'leadreg' else 0 for i in latest_lead_remark]
    walkinfollowup = [i.lead if hasattr(i, 'status') and i.status == 'walkinfollowup' else 0 for i in latest_lead_remark]
    walkinreg = [i.lead if hasattr(i, 'status') and i.status == 'walkinreg' else 0 for i in latest_lead_remark]
    walkindeclaration = [i.lead if hasattr(i, 'status') and i.status == 'walkindeclaration' else 0 for i in latest_lead_remark]
    walkinclose = [i.lead if hasattr(i, 'status') and i.status == 'walkinclose' else 0 for i in latest_lead_remark]

    category_data = [leadclose,
    leadwalkin,
    leadfollowup,
    leadreg,
    walkinfollowup,
    walkinreg,
    walkindeclaration,
    walkinclose]

    

    category_names = ['leadclose', 'leadwalkin', 'leadfollowup', 'leadreg', 'walkinfollowup', 'walkinreg', 'walkindeclaration', 'walkinclose']

    category_count = [len(i) if any(i) else 0 for i in category_data]

    max_cat_data = max(category_count) + 5
    # min_cat_data = min(category_count) 
    # print('Number of student in by category',category_count)


    context = {
        'emps': emps,
        'leads': leads,
        'total_col': total_col,
        # 'follow_leads': follow_leads,
        # 'leads_seven': leads_seven,
        'seven_days': seven_days,
        'seven_data': seven_data,
        'min_data': min_data,
        'max_data': max_data,
        'month_course': month_course,
        'month_collection': month_collection,
        'min_col': min_col,
        'max_col': max_col,
        'morning_report': morning_report,
        'category_names': category_names,
        'category_count': category_count,
        'max_cat_data': max_cat_data,
        'month_records': month_records,
        'records_and_targets': records_and_targets,
        # 'min_cat_data': min_cat_data,
        # 'month_targets': month_targets,
        # 'target_mails_monthly': target_mails_monthly,
        # 'target_messages_monthly': target_messages_monthly,
        # 'target_calls_monthly': target_calls_monthly,
        # 'target_online_submissions_monthly': target_online_submissions_monthly,
        # 'target_follow_ups_monthly': target_follow_ups_monthly,
        # 'emp_monthly_records': emp_monthly_records,
        # 'max_records_by_category': max_records_by_category,
        # 'min_records_by_category': min_records_by_category,
        # 'total_mails_monthly': total_mails_monthly,
        # 'total_messages_monthly': total_messages_monthly,
        # 'total_calls_monthly': total_calls_monthly,
        # 'total_online_submissions_monthly': total_online_submissions_monthly,
        # 'total_follow_ups_monthly': total_follow_ups_monthly,
        # 'emp_record_categories': emp_record_categories,
        # 'emp_records_by_category': emp_records_by_category,
        # 'emp_targets_by_category':emp_targets_by_category,
    }
    # if any(follow_leads):
    #     context['follow_leads'] = follow_leads

    return render(request, 'pages/my_panel.html', context)


# def notification(request):
#     follow_leads = Lead.objects.all().filter(is_counseled=True).filter(next_follow_up_date__lte=datetime.date.today())
    
#     context = {'follow_leads': follow_leads,}

#     return render(request, 'partials/_dash_navbar.html', context)


@login_required(login_url='admin:login')
def profile(request):
    emps = Employee.objects.all()

    current_user = request.user
    emp = Employee.objects.filter(name=current_user)
  
    context = {
        'emps': emps,
        'current_user': current_user,
        'emp': emp,
    }
    return render(request, 'pages/myprofile.html', context)


@login_required(login_url='admin:login')
def my_reports(request):
    emp = request.user
    try:
        emps = emp.profile.get_descendants(include_self=True)
    except:
        emps = Employee.objects.none()
    leads = Lead.objects.all()
    latest_lead_remark = [i.lead_remarks.last() for i in leads]
    registered_lead_ids = [i.lead.id for i in latest_lead_remark if hasattr(i, 'status') and i.status == 'walkinreg']
    # try:
    registered_leads = Lead.objects.all().filter(id__in=registered_lead_ids).filter(assigned_to__in=emps)
    # except:
    #     registered_leads = Lead.objects.none()
    context = {
        'registered_leads': registered_leads,
    }
    return render(request, 'pages/my_reports.html', context)


@login_required(login_url='admin:login')
def notifications(request):
    info = Lead.objects.all().order_by('-generation_at').filter(assigned_to_id=request.user.id).filter(is_counseled=False)
    try:
        success = Lead.objects.filter(is_counseled=True).filter(status='Walk in registered')
    except:
        success = Lead.objects.none()
    current_user = request.user.id
    context = {
        'info': info,
        'success': success,
        'current_user': current_user,
    }
    return render(request, 'pages/notifications.html', context)


@login_required(login_url='admin:login')
def icons(request):
    return render(request, 'pages/icons.html')


@login_required(login_url='admin:login')
def logout_view(request):
    logout(request)
    return render(request, 'pages/index.html')

def dts(request):
    if request.method == 'POST':
        report = TargetDTS()
        report.task = ''
        for i in range(1, 9):
            if request.POST.get('target{i}') :
                report.task += request.POST.get('target{i}')
               
                report.save()               
                return render(request, 'pages/my_panel.html')  

    else:
            return render(request,'pages/about.html')





def sales_last_seven_days(request):
    delta = 0
    todays_day = date.today().weekday()
    registered_leads = [i if not i==None or i==0 else 0 for i in Lead.objects.values_list('course_fee', flat=True).filter(status='Walk in registered')]   
    context = {

        'colls': registered_leads
    }
    return render(request, 'pages/collection_data.html', context)



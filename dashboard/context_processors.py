from leads.models import Lead, LeadRemarks
from datetime import date, timedelta
from django.db.models import Q



def notification(request):
    # follow_leads = Lead.objects.all().filter(is_counseled=True).filter(next_follow_up_date__lte=datetime.date.today())

    # follow_leads = LeadRemarks.objects.all().filter(next_follow_up_date__lte=date.today()).latest('next_follow_up_date')
    # unregistered_leads = [l.lead.id for l in follow_leads if l.status !='walkinreg' or l.status !='leadreg']
    # follow_leads = Lead.objects.filter(id__in=unregistered_leads)
    follow_leads = Lead.objects.all().filter(lead_remarks__next_follow_up_date=date.today()).filter(Q(lead_remarks__status='leadfollowup') | Q(lead_remarks__status='walkinfollowup'))

    context = {'follow_leads': follow_leads,}
    return context
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Lead, CorporateAndInstitutionLead

# from .forms import LeadForm, RemarksModelFormset

# Create your views here.
def new_leads(request):
    leads = Lead.objects.all().filter(is_counseled=False)

    paginator = Paginator(leads, 3)
    page = request.GET.get('page')
    paged_leads = paginator.get_page(page)

    context = {
        'leads': paged_leads
    }
    return render(request, 'leads/listings.html', context)

def all_leads(request):
    # leads = Lead.objects.all().filter(assigned_to_id=request.user.profile.id)
    leads = Lead.objects.all()
    paginator = Paginator(leads, 3)
    page = request.GET.get('page')
    paged_leads = paginator.get_page(page)

    context = {
        'leads': paged_leads
    }
    return render(request, 'leads/all_leads.html', context)

# def listing(request):
#     return render(request, 'leads/listing.html')


def search(request):
    return render(request, 'leads/search.html')


# def generate(response):
#     if response.method == "POST":
#         form = RemarksModelFormset(response.POST)
#         if form.is_valid:
#             form.save()
#         return redirect('generate')
#     else:
#         form = RemarksModelFormset()
#     return render(response, 'pages/generation.html', {'form':form})

def single_lead(request, id):
    lead = get_object_or_404(Lead, pk=id)

    context = {
        'lead': lead,
    }

    return render(request, 'leads/listing.html', context)


def show_quotation(request, id):
    quotation = get_object_or_404(CorporateAndInstitutionLead, pk=id)

    context = {
        'quotation': quotation
    }

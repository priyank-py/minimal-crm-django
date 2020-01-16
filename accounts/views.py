from django.shortcuts import render, get_object_or_404
from .models import Invoice, Bill, InstallmentData, Quotation, QuotationRatesAndTerms
from leads.models import CorporateAndInstitutionLead
from django.core.mail import EmailMessage
from django.http import HttpResponse

#for pdf:
from weasyprint.fonts import FontConfiguration
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML


# Create your views here.
def invoices(request):
    get_invoices = Invoice.objects.all()
    get_both = [(Bill.objects.all().filter(invoice=i), i) for i in get_invoices]
    
    context = {'get_both': get_both,}
    return render(request, 'pages/invoices.html', context)


def lead_invoice(request, id):
    invoice = get_object_or_404(Invoice, pk=id)
    installments = InstallmentData.objects.order_by('-id').filter(invoice=invoice)
    bills = Bill.objects.order_by('-id').filter(invoice=invoice)
    print(dir(HTML))

    context = {
        'invoice': invoice,
        'bills': bills,
        'installments': installments,
    }

    return render(request, 'commerce/invoice.html', context)


def each_bill(request, id):
    bill = get_object_or_404(Bill, pk=id)
    pay_method = bill.payment_option
    if pay_method == 'cash':
        cash = True
    else:
        cash = False
    if pay_method == 'cheque':
        cheque = True
    else:
        cheque = False
    context = {
        'bill': bill,
        'cash': cash,
        'cheque': cheque,
    }
    return render(request, 'commerce/bill.html', context)


def all_quotation(request):
    quotes = Quotation.objects.all()
    context = {
        'quotes': quotes,
    }
    return render(request, 'pages/quotes.html')


def quotation(request, id):
    quote = get_object_or_404(Quotation, pk=id)
    rates = QuotationRatesAndTerms.objects.all().filter(quotation=quote)
    rates = enumerate(rates)
    context = {
        'quote': quote,
        'rates': rates,
    }

    return render(request, 'commerce/quote.html', context)


# def sendRecieptEmail(request,emailto):
#    res = send_mail("hello paul", "comment tu vas?", "factscred@gmail.com", [emailto])
#    return HttpResponse('%s'%res)

def invoice_to_pdf_view(request, id):

    invoice = get_object_or_404(Invoice, pk=id)
    installments = InstallmentData.objects.order_by('-id').filter(invoice=invoice)
    bills = Bill.objects.order_by('-id').filter(invoice=invoice)
    # print(dir(HTML))

    context = {
        'invoice': invoice,
        'bills': bills,
        'installments': installments,
    }

    html_string = render_to_string('commerce/invoice.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/invoices/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/invoices/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        msg = EmailMessage(f'Invoice of {invoice.lead.lead_name} for {invoice.enquired_for}', 'Check the attachment for the invoice of the candidate', 'info@red18tech.com', ['athirupan.kk@gmail.com'])
        msg.content_subtype = "html"  
        msg.attach_file(f'media/invoices/pdf-{id}.pdf')
        msg.send()


        return response

    return response

def bill_to_pdf_view(request, id):

    bill = get_object_or_404(Bill, pk=id)
    context = {'bill': bill}

    html_string = render_to_string('commerce/bill.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/bills/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/bills/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
        email_to = ['athirupan.kk@gmail.com']
        if quote.email:
            email_to.append(bill.invoice.lead.lead_email)
        msg = EmailMessage(f'Red18tech: Bill for {bill.invoice.enquired_for} course', f'Dear {bill.invoice.lead.lead_name},\nPlease check the attachment for your bill\nThanks & regards\nRed18tech', 'info@red18tech.com', email_to)
        msg.content_subtype = "html"  
        msg.attach_file(f'media/bills/pdf-{id}.pdf')
        msg.send()


        return response

    return response


def quotation_to_pdf_view(request, id):

    quote = get_object_or_404(Quotation, pk=id)
    rates = QuotationRatesAndTerms.objects.all().filter(quotation=quote)
    rates = enumerate(rates)
    context = {
        'quote': quote,
        'rates': rates,
    }

    html_string = render_to_string('commerce/quote.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/Quotations/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/Quotations/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="quotation.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)
        email_to = ['athirupan.kk@gmail.com']
        if quote.email:
            email_to.append(quote.email)
        msg = EmailMessage(quote.subject, f'Dear {quote.client_name},\nCheck the attachement for the quotation', 'info@red18tech.com', email_to)
        msg.content_subtype = "html"  
        msg.attach_file(f'media/Quotations/pdf-{id}.pdf')
        msg.send()


        return response

    return response
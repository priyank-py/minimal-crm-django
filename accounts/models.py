from django.db import models
from leads.models import Lead, CorporateAndInstitutionLead
from employees.models import Employee
from django.utils import timezone
from django.utils.translation import gettext as _
from math import ceil

# Create your models here.

def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('-id').last()
    if not last_invoice:
        return "{0:0=6d}".format(1)
    invoice_number = last_invoice.invoice_number
    booking_int = int(invoice_number[3:])
    new_booking_int = booking_int + 1
    new_booking_id = "{0:0=6d}".format(new_booking_int)
    return new_booking_id

class Invoice(models.Model):
    CHOICES = (('Java','Java'),('Python','Python'),('Php','Php'))
    lead = models.ForeignKey(Lead, verbose_name=_("Lead"), related_name='lead_invoice', on_delete=models.CASCADE)
    # dated = models.DateField(blank=True, null=True)
    enquired_for = models.CharField(_("Service Taken"), max_length=50, blank=True, null=True)
    batchstartdate = models.DateField(_("Batch Start Date"), blank=True, null=True, default=None)
    counselor = models.ForeignKey(Employee, verbose_name=_("Counseled by"), on_delete=models.CASCADE)
    invoice_number = models.CharField(_("Invoice#"), max_length=50, default=increment_invoice_number, editable=False, unique=True)
    
    # bal_amount = models.IntegerField(_("Due Amount"), blank=True, null=True)
    # due_date = models.DateField(_("Dues pay date"), blank=True, null=True)
    add_fee = models.IntegerField(_("Admission Fee"), blank=True,null=True)
    course_ware_fee = models.IntegerField(blank=True,null=True)
    tution_fee = models.IntegerField(blank=True,null=True)
    project_fee = models.IntegerField(blank=True,null=True)
    late_fee = models.IntegerField(blank=True,null=True)
    exam_fee = models.IntegerField(blank=True,null=True)
    other = models.IntegerField(blank=True,null=True)
    # coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    sub_total = models.IntegerField(blank=True,null=True)
    gst = models.CharField(max_length=50,blank=True,null=True)
    g_total = models.IntegerField(_("Grand Total"), blank=True,null=True)
    amount_words = models.CharField(_("Amount in word"), max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # test  = self.counselor.branch_city[:3].upper() 
        
        if not self.invoice_number[:3] == self.counselor.branch_city[:3].upper():
            self.invoice_number = self.counselor.branch_city[:3].upper() + self.invoice_number


        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        values = [self.add_fee, self.course_ware_fee, self.tution_fee, self.project_fee, self.exam_fee, self.late_fee, self.other]
        self.sub_total = ceil(sum([i for i in values if i != None]))
        self.gst = self.sub_total * 0.18
        self.g_total = ceil(self.sub_total + self.gst)
        self.amount_words = num2words(self.g_total)
        # self.bill_number = self.invoice.invoice_number + 
        super(Invoice, self).save(*args, **kwargs)

    @property
    def lead_name(self):
        return self.lead.lead_name

    def __str__(self):
        if self.invoice_number:
            return f'{self.invoice_number}'
        else:
            return f'{self.lead}'
 

class InstallmentData(models.Model):
    
    invoice = models.ForeignKey(Invoice, verbose_name=_(""), on_delete=models.CASCADE)
    installment_date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    installment_amount = models.IntegerField(_("Amount"), blank=True, null=True)
    

def increment_bill_number():
    
    last_bill = Bill.objects.all().order_by('-id').last()
    if not last_bill:
        return "{0:0=2d}".format(1) 
    bill_number = last_bill.bill_number
    booking_int = int(bill_number[-2:])
    new_booking_int = booking_int + 1
    new_booking_id = "{0:0=2d}".format(new_booking_int)
    return new_booking_id


class Bill(models.Model):
    
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))
    
    cheque_status_options = (('cleared', 'Cleared'), ('pending', 'Pending'), ('failed', 'Failed'))
    invoice = models.ForeignKey(Invoice, related_name='source_invoice', on_delete=models.CASCADE, blank=True, null=True)
    bill_number = models.CharField(_("Bill#"), max_length=50, default=increment_bill_number, editable=False, null=True, blank=True, unique=True)
    
    # bill_number = models.PositiveSmallIntegerField(_("Bill#"), blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True, default=timezone.now)
    # client = models.CharField(max_length=30,blank=True,null=True)
    payment_option = models.CharField(_("Pay Option"), max_length=30, choices=pay_options, blank=True, null=True)
    recieve_amount = models.IntegerField(_("Recieved Amount"), blank=True, null=True)
    amount_in_word = models.CharField(_("Amount in Words"), max_length=50, blank=True, null=True)    

    #crdname=models.CharField(max_length=200)
    credit_card_no = models.CharField(_("Credit/Debit Card No."), blank=True, null=True, default=None, max_length=20)
    dd_no = models.CharField(_("DD No."), blank=True, null=True, max_length=20, default=None)
    cheque_no = models.CharField(blank=True, null=True, max_length=20, default=None)
    drawn_on = models.DateField(_("Drawn on"), auto_now=False, auto_now_add=False, blank=True, null=True, default=timezone.now)
    bank_name = models.CharField(_("Bank name"), max_length=50, blank=True, null=True)
    bank_branch = models.CharField(_("Bank Branch Name"), max_length=50, blank=True, null=True)
    cheque_status = models.CharField(_("Cheque Status"), max_length=10, choices=cheque_status_options, blank=True, null=True)
    change = models.IntegerField(_("Change amount"), blank=True, null=True)
    tens = models.IntegerField(_("Rs. 10 notes"), blank=True, null=True)
    twenties = models.IntegerField(_("Rs. 20 notes"), blank=True, null=True)
    fiftys = models.IntegerField(_("Rs. 50 notes"), blank=True, null=True)
    hundreds = models.IntegerField(_("Rs. 100 notes"), blank=True, null=True)
    two_hundreds = models.IntegerField(_("Rs. 200 notes"), blank=True, null=True)
    five_hundreds = models.IntegerField(_("Rs. 500 notes"), blank=True, null=True)
    two_thousands = models.IntegerField(_("Rs. 2000 notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")

    
    def save(self, *args, **kwargs):
        # if not self.id:
        #     m = Bill.objects.all().order_by("-id")[0]
            # self.id = self.invoice.invoice_number + "{0:0=2d}".format(m if m is not None else 1)

        def increase_bill_number():      
            last_bill = Bill.objects.all().order_by('-id').filter(bill_number__contains=self.invoice.invoice_number).last()
            if not last_bill:
                return "{0:0=2d}".format(1) 
            bill_number = last_bill.bill_number
            booking_int = int(bill_number[-2:])
            new_booking_int = booking_int + 1
            new_booking_id = "{0:0=2d}".format(new_booking_int)
            return new_booking_id



        if self.recieve_amount and self.invoice.invoice_number != self.bill_number[:-2]:
            self.bill_number = self.invoice.invoice_number + increase_bill_number()

        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        try:
            self.amount_in_word = num2words(ceil(self.recieve_amount))
        except:
            self.amount_in_word = 0
        super(Bill, self).save(*args, **kwargs)


    def __str__(self):
        if self.bill_number:
            return f'{self.bill_number}'
        else:
            return f'{self.id}'

    # def get_absolute_url(self):
    #     return reverse("Bill_detail", kwargs={"pk": self.pk})



class ClientInvoice(models.Model):

    lead = models.ForeignKey(CorporateAndInstitutionLead, verbose_name=_("Client"), on_delete=models.CASCADE)
    enquired_for = models.CharField(_("Service Taken"), max_length=50, blank=True, null=True)
    batchstartdate = models.DateField(_("Batch Start Date"), blank=True, null=True, default=None)
    counselor = models.ForeignKey(Employee, verbose_name=_("BDE Name"), on_delete=models.CASCADE)
    
    add_fee = models.IntegerField(_("Admission Fee"), blank=True,null=True)
    course_ware_fee = models.IntegerField(blank=True,null=True)
    tution_fee = models.IntegerField(blank=True,null=True)
    project_fee = models.IntegerField(blank=True,null=True)
    late_fee = models.IntegerField(blank=True,null=True)
    exam_fee = models.IntegerField(blank=True,null=True)
    other = models.IntegerField(blank=True,null=True)
    # coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    sub_total = models.IntegerField(blank=True,null=True)
    gst = models.CharField(max_length=50,blank=True,null=True)
    g_total = models.IntegerField(_("Grand Total"), blank=True,null=True)
    amount_words = models.CharField(_("Amount in word"), max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        values = [self.add_fee, self.course_ware_fee, self.tution_fee, self.project_fee, self.exam_fee, self.late_fee, self.other]
        self.sub_total = ceil(sum([i for i in values if i != None]))
        self.gst = self.sub_total * 0.18
        self.g_total = ceil(self.sub_total + self.gst)
        self.amount_words = num2words(self.g_total)
        super(ClientInvoice, self).save(*args, **kwargs)

    @property
    def lead_name(self):
        return self.lead.name

    def __str__(self):
        return f'{self.lead}'
    

    class Meta:
        verbose_name = _("ClientInvoice")
        verbose_name_plural = _("ClientInvoices")

    def __str__(self):
        return self.name

class ClientInstallmentData(models.Model):

    invoice = models.ForeignKey(ClientInvoice, verbose_name=_(""), on_delete=models.CASCADE)
    payment_status = ((True, 'Paid'), (False, 'Unpaid'))
    installment_date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    installment_amount = models.IntegerField(_("Amount"), blank=True, null=True)
    paid = models.BooleanField(_("Payment Status"), choices=payment_status, default=False, blank=True, null=True)



class ClientBill(models.Model):
 
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))
    cheque_status_options = (('cleared', 'Cleared'), ('pending', 'Pending'), ('failed', 'Failed'))
    invoice = models.ForeignKey(ClientInvoice, verbose_name=_(""), on_delete=models.CASCADE)
    bill_date = models.DateField(blank=True, null=True, default=timezone.now)
    # client = models.CharField(max_length=30,blank=True,null=True)
    payment_option = models.CharField(_("Pay Option"), max_length=30, choices=pay_options)
    recieve_amount = models.IntegerField(_("Recieved Amount"), blank=True, null=True)
    amount_in_word = models.CharField(_("Amount in Words"), max_length=50, blank=True, null=True)    

    #crdname=models.CharField(max_length=200)
    credit_card_no = models.CharField(_("Credit/Debit Card No."), blank=True, null=True, default=None, max_length=20)
    dd_no = models.CharField(_("DD No."), blank=True, null=True, max_length=20, default=None)
    cheque_no = models.CharField(blank=True, null=True, max_length=20, default=None)
    drawn_on = models.DateField(_("Drawn on"), auto_now=False, auto_now_add=False, blank=True, null=True, default=timezone.now)
    bank_name = models.CharField(_("Bank name"), max_length=50, blank=True, null=True)
    bank_branch = models.CharField(_("Bank Branch Name"), max_length=50, blank=True, null=True)
    cheque_status = models.CharField(_("Cheque Status"), max_length=10, choices=cheque_status_options, blank=True, null=True)
    tens = models.IntegerField(_("Rs. 10 notes"), blank=True, null=True)
    twenties = models.IntegerField(_("Rs. 20 notes"), blank=True, null=True)
    fiftys = models.IntegerField(_("Rs. 50 notes"), blank=True, null=True)
    hundreds = models.IntegerField(_("Rs. 100 notes"), blank=True, null=True)
    two_hundreds = models.IntegerField(_("Rs. 200 notes"), blank=True, null=True)
    five_hundreds = models.IntegerField(_("Rs. 500 notes"), blank=True, null=True)
    two_thousands = models.IntegerField(_("Rs. 2000 notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("Client Bill")
        verbose_name_plural = _("Client Bills")

    
    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        self.amount_in_word = num2words(ceil(self.recieve_amount))
        super(ClientBill, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.invoice.id}'

class Quotation(models.Model):
    date = models.DateField(_("Dated"), auto_now=False, auto_now_add=False, default=timezone.now)
    client_name = models.CharField(_("Client Name"), max_length=50)
    client_address = models.TextField(_("To"), blank=True, null=True)
    email = models.EmailField(_("Client Email"), max_length=254, blank=True, null=True)

    subject = models.CharField(_("Subject"), max_length=140, null=True, blank=True)
    reference = models.CharField(_("Ref"), max_length=80, null=True, blank=True)
    total_amount = models.PositiveIntegerField(_("Total Amount"), blank=True, null=True)
    amount_in_word = models.CharField(_("Amount in Words"), max_length=50, blank=True, null=True)
    company_terms = models.TextField(_("Company Terms & Conditions"), null=True, blank=True)
    client_terms = models.TextField(_("Client's Terms & Conditions"), null=True, blank=True)
    signature = models.ImageField(_("Upload Authorised Signator"), upload_to=None, height_field=None, width_field=None, blank=True, null=True, max_length=None)
    
    def __str__(self):
        return f'{self.client_name}'

    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        self.amount_in_word = num2words(ceil(self.total_amount))
        super(Quotation, self).save(*args, **kwargs)


class QuotationRatesAndTerms(models.Model):

    quotation = models.ForeignKey(Quotation, verbose_name=_("Quotation"), related_name="quote_details", on_delete=models.CASCADE)
    item_description = models.CharField(_("Item Description"), max_length=80, null=True, blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(_("Tax (18%)"), max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("QuotationRatesAndTerms")
        verbose_name_plural = _("QuotationRatesAndTermss")

    def __str__(self):
        return self.quotation.client_name

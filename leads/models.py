from django.db import models
import datetime
from employees.models import Employee
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
available_status = (('leadclose', 'Lead Closed'), ('leadwalkin', 'Lead walked in'), ('leadfollowup', 'Leads follow up'), ('leadreg', 'Lead Registered'), ('walkinfollowup', 'Walk in follow up'), ('walkinreg', 'Walk in registered'), ('walkindeclaration', 'Walk declaration Signed'), ('walkinclose', 'Walk in closed'))
YEAR_CHOICES = [(i, i) for i in range(2000, (int(datetime.datetime.now().year)+4))]
enquired_choices = (('course', 'Course'), ('project', 'Project'), ('internship', 'Internship'), ('jobassured', 'Job Assured Training'), ('onlyjob', 'Only Job'))
tech_choices = (('python', 'Python'), ('java', 'Java'), ('datascienc', 'Data Science'), ('webpython', 'Web Development - Python'), ('webphp', 'Web Development - PHP'), ('webjava', 'Web Development - Java'))

class Lead(models.Model):

    lead_name = models.CharField(max_length=150)
    lead_email = models.EmailField(null=True, blank=True)
    lead_phone = models.CharField(max_length=20)
    campaign_remarks = models.CharField(max_length=255, null=True, blank=True)
    enquired_for = models.CharField(max_length=250, choices=enquired_choices, default='', null=True, blank=True)
    technology_based = models.CharField(max_length=250, null=True, blank=True)
    skills_known = TaggableManager(verbose_name='technologies known', blank=True)
    
    course_fee = models.IntegerField(null=True, blank=True, default=0)
    
    # assigned_to = models.CharField(max_length=200, choices=available_status, default='')
    under_graduation = models.CharField(blank=True, max_length=200)
    year_of_passing_UG = models.IntegerField(null=True, blank=True, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    marks_UG = models.FloatField(null=True, blank=True, validators=[MinValueValidator(39.99), MaxValueValidator(100)])
    post_graduation = models.CharField(blank=True, max_length=200)
    year_of_passing_PG = models.IntegerField(null=True, blank=True, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    marks_PG = models.FloatField(null=True, blank=True, validators=[MinValueValidator(39.99), MaxValueValidator(100)])
    location = models.CharField(max_length=200, null=True, blank=True)
    # remarks = models.TextField(null=True, blank=True)
    
    # final_report = models.CharField(max_length=150, null=True, blank=True)
    lead_image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_counseled = models.BooleanField(default=False)
    # user = models.ForeignKey(User,related_name='lead',related_query_name='lead',on_delete=models.CASCADE)
    generation_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)    
    counselor_name = models.CharField(max_length=100, null=True, blank=True)
    assigned_to = models.ForeignKey(Employee, related_name='counselor', on_delete=models.DO_NOTHING, blank=True, null=True)
     


    def __str__(self):
        return self.lead_name

from .models import Lead

class LeadRemarks(models.Model):

    lead = models.ForeignKey(Lead, related_name='lead_remarks', on_delete=models.DO_NOTHING)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    next_follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=available_status, default='', null=True, blank=True)

    def current_follow_up_date(self, instance):
        try:
            return self.instance.next_follow_up_date.last()
        except:
            return None

    def current_status(self):
        return self.lead.status

    def __str__(self):
        return self.lead.lead_name


class CorporateAndInstitutionLead(models.Model):

    agreement_status = ((True, 'Signed'), (False, 'Not Signed'))

    name = models.CharField(_("Corporate/Institution Name"), max_length=50)
    contact_person = models.CharField(_("Contact Person Name"), max_length=50)
    cp_designation = models.CharField(_("Contact Person Designation"), max_length=50, blank=True, null=True)
    cp_phone = models.CharField(_("Contact Person Phone Number"), max_length=50, blank=True, null=True)
    cp_alternative = models.CharField(_("Contact Person Alternative  Number"), max_length=50)
    cp_email = models.EmailField(_("Contact Person Email"), max_length=254, blank=True, null=True)
    institution_or_corporate_website = models.URLField(_("Website of Corporate/Institution"), max_length=200, blank=True, null=True)
    enquired_for = models.CharField(max_length=50)
    billing_amount = models.IntegerField(_("Collections Amount"), blank=True, null=True)
    agreement_signed = models.BooleanField(choices=agreement_status, default="", blank=True, null=True)
    agreement_copy = models.FileField(_("Agreement Copy"), upload_to='agreements/%Y/%m/%d/', max_length=100, blank=True, null=True)
    quotation = models.FileField(_("Quotation Copy"), upload_to='quotations/%Y/%m/%d/', max_length=100)
    quotation_dated = models.DateField(_("Quotation preperation date"), auto_now=False, auto_now_add=False)
    bde_name = models.ForeignKey(Employee, verbose_name=_("BDE Name"), on_delete=models.CASCADE)

class CorporateAndInstitutionLeadRemark(models.Model):

    statuses = (('hot', 'Hot'), ('warm', 'Warm'), ('cold', 'Cold'), ('converted', 'Converted'), ('closed', 'Closed'))

    corporate_or_institution_lead = models.ForeignKey(CorporateAndInstitutionLead, related_name='corp_lead_remark', on_delete=models.DO_NOTHING)
    remark = models.CharField(_("remarks"), max_length=200, blank=True, null=True)
    follow_up_date = models.DateField(_("Follow-up Date"), default='', null=True, blank=True)
    lead_status = models.CharField(_("lead status"), max_length=50, choices=statuses, blank=True, null=True)


from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Employee(MPTTModel):
    
    STANDARD = 'STD'
    TEAM_LEADER = 'TL'
    MANAGER = 'MGR'
    SR_MANAGER = 'SRMGR'
    PRESIDENT = 'PRES'

    EMPLOYEE_TYPES = (
        (STANDARD, 'base employee'),
        (TEAM_LEADER, 'team leader'),
        (MANAGER, 'manager'),
        (SR_MANAGER, 'senior manager'),
        (PRESIDENT, 'president'))

    positions_available = (
        ('telecaller', 'Telecaller'),
        ('frontdesk', 'Front Desk'),
        ('counselor', 'Counselor'),
        ('bde', 'BDE'),
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('seniormanager', 'Senior Manager'),
    )

    our_locations = (('Bangalore', 'Bangalore'), ('Coimbatore', 'Coimbatore'))
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(max_length=1000, upload_to='photos/%Y/%m/%d/', blank=True, null=True) 
    postion = models.CharField(max_length=100, choices=positions_available, blank=True, null=True)
    role = models.CharField(max_length=25, choices=EMPLOYEE_TYPES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    hire_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    branch_city = models.CharField(max_length=200, choices=our_locations, default='', blank=True, null=True)
    is_eom = models.BooleanField(blank=True, null=True, default=False)
    parent = TreeForeignKey('self',blank=True, null=True, related_name='employee', on_delete=models.DO_NOTHING)
    # profile = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     super().save(*args,**kwargs)

    #     img = Image.open(self.photo.path)
    #     if img.height> 300 or img.width>300:
    #         output_size  = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)
#     instance.employee.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employee.save()


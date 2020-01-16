from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class EmployeeTargetInline(admin.TabularInline):
    model = MonthlyCustomTarget
    
    can_delete = False
    fk_name='monthly_target'
    extra = 1
    # max_num = 1
    min_num = 1



class MonthlyTargetAdmin(admin.ModelAdmin):
    list_display = ('position', 'month')
    list_display_links = ('position',)
    list_filter = ('position',)
    readonly_fields = ('month',)

    class Meta:
        model = MonthlyTarget
        fields = '__all__'

    inlines = (EmployeeTargetInline, )
    

class EmpCustomRecordAdmin(admin.TabularInline):
    model = EmpCustomRecord
    extra = 1


class EmpRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'submitted_on')
    # list_display_links = ('lead_id', 'lead_name', 'enquired_for')
    list_filter = (('employee'), ('submitted_on', DateTimeRangeFilter))
    # # list_editable = ('is_counseled', 'next_follow_up_date',)
    search_fields = ('employee', 'submitted_on')
    

    actions = ["export_as_csv"]
    
    class meta:
        model = EmpRecord
        fields = '__all__'

    inlines = ( EmpCustomRecordAdmin,)

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class TargetDataTabularInline(admin.TabularInline):
    model = TargetData
    extra = 1

class AchievedDataTabularInline(admin.TabularInline):
    model = AchievedData
    extra = 1

class DTSAdmin(admin.ModelAdmin):
    list_display = ('employee', 'dated')
    search_fields = ('employee', 'dated')
    list_filter = (('employee'), ('dated', DateTimeRangeFilter))
   
    class Meta:
        model = DTS
        fields = '__all__'
    inlines = (TargetDataTabularInline, AchievedDataTabularInline,)
    

admin.site.register(EmpRecord, EmpRecordAdmin)
admin.site.register(DTS, DTSAdmin)
admin.site.register(MonthlyTarget, MonthlyTargetAdmin)
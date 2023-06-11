from django.contrib import admin
from home.models import Setting, ContactMessage, FAQ, OpeningHour, SpecialDay

admin.site.site_header = 'Cafe Database'
# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','status']
    list_filter = ['status']


class SpecialDayAdmin(admin.ModelAdmin):
    list_display = ['title', 'holiday_date', 'weekDay',]

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['Opening_day', 'Opening_Hour_starts', 'Opening_Hour_ends', 'WeekDayToday', ]


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(SpecialDay, SpecialDayAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)





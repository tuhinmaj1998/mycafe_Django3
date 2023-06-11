from django.contrib import admin

from delivery.models import DeliveryManagement, DeliveryPartnerProfile, DeliveryPartnerSchedule, DeliveryLimit



class DeliveryLimitAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_order_to_assign', 'maxDistance_1trip_KM', 'maxWeight_1trip_GRAM', 'maxVolume_1trip_CC', ]


class DeliveryManagementAdmin(admin.ModelAdmin):
    list_display = ['bookingInfo', 'deliveryStatus', 'timestamp', 'delivery_address', ]
    list_filter = ['deliveryStatus']


class DeliveryPartnerProfileAdmin(admin.ModelAdmin):
    list_display = ['deliveryPartner', 'deliveryPartnerStatus']
    list_filter = ['deliveryPartnerStatus']

class DeliveryPartnerScheduleAdmin(admin.ModelAdmin):
    list_display = ['delivery_Partner', 'readyOrder', 'scheduleTime','delivery_address', 'status', ]


admin.site.register(DeliveryLimit, DeliveryLimitAdmin)
admin.site.register(DeliveryManagement, DeliveryManagementAdmin)
admin.site.register(DeliveryPartnerProfile, DeliveryPartnerProfileAdmin)
admin.site.register(DeliveryPartnerSchedule, DeliveryPartnerScheduleAdmin)






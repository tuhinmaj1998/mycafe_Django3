from django.contrib import admin

# Register your models here.
from user.models import UserProfile, Subscriber, Wallet, WalletTransaction, UserAddress


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone','image_tag']



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['plan', 'code', 'user_name', 'start', 'planExipry', 'status']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'cashBackTotal']


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transactionAmount', 'cashBackCoupon', 'timeIssued', 'status_sign']


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'latitude', 'longitude']



admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(UserAddress, UserAddressAdmin)



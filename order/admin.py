from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order, paytm_data


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity','price', 'amount','user']
    list_filter = ['user', 'quantity']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'locationAddress' ,'first_name', 'last_name','phone','total','status', 'code', 'net_weight_gram', ]
    list_filter = ['status']
    readonly_fields = ('user','phone','first_name','ip', 'last_name', 'total')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount', 'total_weight_gram', ]
    list_filter = ['user']

class paytmAdmin(admin.ModelAdmin):
    list_display = ['MID', 'INDUSTRY_TYPE_ID', 'WEBSITE', 'CHANNEL_ID', 'CALLBACK_URL']


admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(paytm_data, paytmAdmin)


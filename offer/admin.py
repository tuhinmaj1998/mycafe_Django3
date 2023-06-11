from django import forms
from django.contrib import admin

# Register your models here.
from offer.models import Subscription, Subscription_Duration, Fine, ProductDiscount, CashBackCoupon
from product.models import Variants


class SubscriptionInline(admin.TabularInline):
    model = Subscription_Duration
    #can_delete = False
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'rank', 'create_at', 'color_tag', 'slug']
    inlines = [SubscriptionInline]
    prepopulated_fields = {'slug': ('title',)}


class Subscription_DurationAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'percentage', 'limit_amount', 'price', 'slug']
    list_filter = ['duration', 'percentage']
    prepopulated_fields = {'slug': ('title',)}

class FineAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'percentage', 'minimumAmount', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ProductDiscountForm(forms.ModelForm):

    class Meta:
        model = ProductDiscount
        fields = ['product', 'variant']

    def __init__(self, *args, **kwargs):
        super(ProductDiscountForm, self).__init__(*args, **kwargs)
        self.fields['variant'].queryset = Variants.objects.filter(
            product_id=self.instance.product_id)

class ProductDiscountAdmin(admin.ModelAdmin):
    """
    Admin Class for 'Movie Category'.
    """

    fieldsets = [

        ('Product Information', {'fields': ['product', 'variant']}),
        ('Discount Information', {'fields': ['discountPercent', 'expiryDate']}),


    ]

    list_display = ('product', 'variant', 'discountPercent', 'expiryDate', 'ActualPrice', 'DiscountPrice', 'expiryDay','expiryHour', )
    #search_fields = ['category__category_name', 'movie_ 'prefix__prefix']
    form = ProductDiscountForm
    #prepopulated_fields = {'slug': ('product',)}


class CashBackCouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'user',  'cashBackLimit', 'cashBackPercent', 'cashBackstatus', 'cashBackexpiryDate', 'expiryDay', 'expiryHour', 'cashBackstatus' ]
    #prepopulated_fields = {'slug': ('title',)}
    list_filter = ['cashBackstatus', 'user']


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Subscription_Duration, Subscription_DurationAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(CashBackCoupon, CashBackCouponAdmin)


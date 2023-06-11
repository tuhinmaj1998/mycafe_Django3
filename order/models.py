from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from product.models import Product, Variants
from user.models import UserAddress


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)  # relation with variant
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']




class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, editable=False )
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)


    #userAddress = models.ForeignKey(UserAddress, models.CASCADE, blank=True, null=True)

    locationAddress = models.CharField(max_length=300, blank=True, null=True)
    houseNo = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)



    priceOffPlan = models.FloatField(default=0.00)
    discountOff = models.FloatField(default=0.00)

    useWallet = models.BooleanField(default=False)
    walletDeduction = models.FloatField(blank=True, null=True, default=0)
    walletDeductionStatus = models.BooleanField(default=False)
    total = models.FloatField()

    cashBackCoupon = models.CharField(blank=True, null=True, max_length=100)
    cashBackIssued = models.FloatField(blank=True, null=True)
    cashBackIssuedStatus = models.BooleanField(default=False)

    status=models.CharField(max_length=10,choices=STATUS,default='Cancelled')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    TXNID = models.CharField(blank=True, max_length=150)
    TXNDATE = models.CharField(blank=True, max_length=150)
    GATEWAYNAME = models.CharField(blank=True, max_length=150)
    BANKTXNID = models.CharField(blank=True, max_length=150)
    BANKNAME = models.CharField(blank=True, max_length=150)
    clientOTP = models.IntegerField(blank=True, default='0000')
    def __str__(self):
        return self.user.first_name + ' : Order No. ' + str(self.id)

    def net_weight_gram(self):
        wts = 0
        order_product = OrderProduct.objects.filter(order_id=self.id)
        for everyOrder_product in order_product:
            wts = wts + everyOrder_product.total_weight_gram()

        return wts

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name', 'phone',  'useWallet', 'locationAddress', 'houseNo', 'latitude', 'longitude', ]

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    productDiscountOff = models.FloatField(default=0.00)
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    def total_weight_gram(self):
        if self.variant == None:
            wt = self.product.weightInGram * self.quantity
        else:
            wt = self.variant.weightInGram * self.quantity

        return wt



class paytm_data(models.Model):
    MID = models.CharField(blank=True, max_length=120)
    INDUSTRY_TYPE_ID = models.CharField(blank=True, max_length=120)
    WEBSITE = models.CharField(blank=True, max_length=120)
    CHANNEL_ID = models.CharField(blank=True, max_length=120)
    CALLBACK_URL = models.CharField(blank=True, max_length=120)
    MKEY = models.CharField(blank=True, max_length=120)

    def __str__(self):
        return 'Paytm: '+ self.MID

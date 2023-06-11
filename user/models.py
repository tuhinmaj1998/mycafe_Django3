from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from offer.models import Subscription_Duration, CashBackCoupon


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')
    deliveryPartner_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Subscriber(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcription = models.ForeignKey(Subscription_Duration, on_delete=models.CASCADE)
    start = models.DateTimeField(blank=True, default=datetime.now)
    code = models.CharField(max_length=10, editable=False)
    status = models.CharField(max_length=10, choices=STATUS, default='Failed')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    paid = models.BooleanField(default=False)
    TXNAMOUNT = models.CharField(blank=True, max_length=50)
    TXNID = models.CharField(blank=True, max_length=150)
    TXNDATE = models.CharField(blank=True, max_length=150)
    GATEWAYNAME = models.CharField(blank=True, max_length=150)
    BANKTXNID = models.CharField(blank=True, max_length=150)
    BANKNAME = models.CharField(blank=True, max_length=150)
    userEnds = models.DateTimeField(auto_now=True)

    #end = models.DateTimeField(default=datetime.now() + timedelta(days=1))

    def __str__(self):
        return self.user.first_name+' :- '+self.subcription.title
        #return str(self.start)

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


    def plan(self):
        return self.subcription.title

    def planExipry(self):
        return self.start + timedelta(days=self.subcription.duration)

class Wallet(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      cashBackTotal = models.FloatField(default=0)
      start = models.DateTimeField(blank=True, default=datetime.now)
      active = models.BooleanField(default=True)

      def __str__(self):
          return self.user.username


class WalletTransaction(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Received', 'Received'),
        ('Failed', 'Failed'),
        ('CashBackApplied', 'CashBackApplied'),
        ('WalletGift', 'WalletGift'),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,)
    byCashBack = models.BooleanField(default=False)
    cashBackCoupon = models.CharField(max_length=100, blank=True, null=True)
    timeIssued = models.DateTimeField(default=datetime.now)
    transactionAmount = models.FloatField(default=0)

    status = models.CharField(max_length=100, choices=STATUS, default='Failed')
    walletGiftStatus = models.BooleanField(default=False)

    start = models.DateTimeField(blank=True, default=datetime.now)
    code = models.CharField(max_length=10, editable=False, default=404)
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    paid = models.BooleanField(default=False)
    TXNAMOUNT = models.CharField(blank=True, max_length=50)
    TXNID = models.CharField(blank=True, max_length=150)
    TXNDATE = models.CharField(blank=True, max_length=150)
    GATEWAYNAME = models.CharField(blank=True, max_length=150)
    BANKTXNID = models.CharField(blank=True, max_length=150)
    BANKNAME = models.CharField(blank=True, max_length=150)


    def __str__(self):
        return self.wallet.user.username

    def status_sign(self):
        if (self.status == 'Paid'):
            return mark_safe('<span>🔻</span>')

        elif (self.status == 'Received') :
            return mark_safe('<span>🟢</span>')

        elif (self.status == 'CashBackApplied') :
            return mark_safe('<span>⚡</span>')

        else:
            return mark_safe('<span>💧</span>')

class WalletForm(ModelForm):
    class Meta:
        model = WalletTransaction
        fields = ['transactionAmount']



class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    locationAddress = models.CharField(max_length=300)
    description = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    houseNo = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    color = models.CharField(max_length=18, default='#000000')

    def __str__(self):
        return self.title










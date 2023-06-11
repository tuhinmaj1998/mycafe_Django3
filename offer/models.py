import time
from datetime import datetime, timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils import timezone
from django.utils.safestring import mark_safe

from product.models import Product, Variants


class Subscription(models.Model):
    title = models.CharField(max_length=100)
    rank = models.IntegerField(validators=[MinValueValidator(1)])
    detail= RichTextUploadingField()
    create_at=models.DateTimeField(auto_now_add=True)
    color_code = models.CharField(max_length=10, blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def color_tag(self):
        if self.color_code is not None:
            return mark_safe('<h3 style="background-color:{}; color:white;">Color </h3>'.format(self.color_code))
        else:
            return ""


class Subscription_Duration(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)])
    detail= models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    limit_amount = models.IntegerField()
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)], default=999)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title



class Fine(models.Model):
    title = models.CharField(max_length=150)
    amount = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    description = models.CharField(blank=True, null=True, max_length=150)
    updated_at = models.DateTimeField(auto_now_add=True)
    percentage = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    minimumAmount = models.IntegerField(verbose_name='Minimum Amount', blank=True, null=True, validators=[MinValueValidator(0)])
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Rule'

    def __str__(self):
        return self.title

class ProductDiscount(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Paused', 'Paused'),
    )
    #title = models.CharField(max_length=150)
    #slug = models.SlugField(null=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True)
    expiryDate = models.DateTimeField(blank=True, default=timezone.now)
    discountPercent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')


    class Meta:
        unique_together = ('product', 'variant',)

    def ActualPrice(self):
        price = 0
        if self.variant == None:
            price = self.product.price
        else:
            price = self.variant.price
        return price

    def DiscountPrice(self):
        price = 0
        if self.variant == None:
            price = self.product.price
        else:
            price = self.variant.price
        return price - price * self.discountPercent / 100

    def expiryDay(self):
        expiry = self.expiryDate
        now = timezone.now()
        daysleft = expiry - now

        return daysleft.days


    def expiryHour(self):
        expiry = self.expiryDate
        now = timezone.now()
        daysleft = expiry - now

        if daysleft.days != 0:
            #return (timezone.now() - timedelta(days=daysleft.days))
            timeleft = (daysleft - timedelta(days=daysleft.days))
            timeleft = ((datetime.min + timeleft).time())

            return timeleft.hour + 1
        else:
            # return (daysleft)
            # daysleft = timedelta(0, 3600)
             timeleft = ((datetime.min + daysleft).time())
             return timeleft.hour
            #return daysleft

    #def expiryMin(self):
        #    eSec = self.expiryDate.second - timezone.now().second
        #    return eSec


    def __str__(self):
        return self.product.title


class CashBackCoupon(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Paused', 'Paused'),
        ('Expied', 'Expired'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(unique=True, max_length=20, validators=[RegexValidator('^[A-Z_0-9 -]*$',
                               'Only uppercase letters, numbers and underscores, hyphens are allowed.')],)
    cashBackLimit = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000000)], default=0)
    cashBackexpiryDate = models.DateTimeField(blank=True, default=timezone.now)
    cashBackPercent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=0)
    cashBackstatus = models.CharField(max_length=10, choices=STATUS, default='Active')
    cashBackTimes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)], default=1)


    def expiryDay(self):
        expiry = self.cashBackexpiryDate
        now = timezone.now()
        CBdaysleft = expiry - now

        return CBdaysleft.days


    def expiryHour(self):
        expiry = self.cashBackexpiryDate
        now = timezone.now()
        daysleft = expiry - now

        if daysleft.days != 0:
            #return (timezone.now() - timedelta(days=daysleft.days))
            timeleft = (daysleft - timedelta(days=daysleft.days))
            timeleft = ((datetime.min + timeleft).time())

            return timeleft.hour
        else:
            # return (daysleft)
            # daysleft = timedelta(0, 3600)
             CBtimeleft = ((datetime.min + daysleft).time())
             return CBtimeleft.hour + 1

    def __str__(self):
        return self.code

    #def save(self, *args, **kwargs):
    #    for field_name in ['code']:
    #        val = getattr(self, field_name, False)
    #        if val:
    #            setattr(self, field_name, val.upper())
    #    super(CashBackCoupon, self).save(*args, *kwargs)










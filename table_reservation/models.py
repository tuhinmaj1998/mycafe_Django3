import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

class Table(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, max_length=30,)
    seat = models.PositiveSmallIntegerField(verbose_name='No. of Seats/Table')
    total = models.IntegerField(verbose_name='Total no. of tables')
    detail= RichTextUploadingField(null=True, blank=True)
    image=models.ImageField(blank=True, upload_to='images/', null=True)
    #availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title

HOUR_OF_DAY_24 = [(i, i) for i in range(00,24)]
HOUR_CHOICE = [(i, i) for i in range(1,16)]


class Time_Table(models.Model):
    parent_table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    hour_selection = models.PositiveSmallIntegerField(unique=True, choices=HOUR_CHOICE, verbose_name='hour(s) of booking')
    price = models.IntegerField()
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, max_length=30)

    def __str__(self):
        return self.title

class Table_Reserve(models.Model):
    user = models.ForeignKey(User, null=True,  on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    time_table = models.ForeignKey(Time_Table, null=True, on_delete=models.SET_NULL)
    on_date = models.DateField()
    time_from = models.PositiveSmallIntegerField(unique=True, choices=HOUR_OF_DAY_24)


    def __str__(self):
        return self.user.username

    def time_to(self):
        return str(self.time_from + self.time_table.hour_selection)




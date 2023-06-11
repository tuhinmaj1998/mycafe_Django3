from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)

    icon = models.ImageField(blank=True,upload_to='images/')

    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name= models.CharField(blank=True,max_length=20)
    email= models.CharField(blank=True,max_length=50)
    subject= models.CharField(blank=True,max_length=50)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject','message']
        widgets = {
            'name'   : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
            'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
            'email'   : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
            'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
        }

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question







HOUR_OF_DAY_24 = [(i,i) for i in range(00,24)]

WEEKDAYS = [
  (0, ("Monday")),
  (1, ("Tuesday")),
  (2, ("Wednesday")),
  (3, ("Thursday")),
  (4, ("Friday")),
  (5, ("Saturday")),
  (6, ("Sunday")),
]

class SpecialDay(models.Model):
    title = models.CharField(max_length=50)
    holiday_date = models.DateField()
    closed = models.BooleanField(default=True)
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, default=0)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, default=23)


    def weekDay(self):
        weekdayNo =  self.holiday_date.weekday()
        return WEEKDAYS[weekdayNo][1]




class OpeningHour(models.Model):
    openingDay = models.PositiveSmallIntegerField(choices=WEEKDAYS, unique=True)
    from_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, default=7)
    to_hour = models.PositiveSmallIntegerField(choices=HOUR_OF_DAY_24, default=23)

    class Meta:
        ordering = ['id', ]

    def Opening_day(self):
        ClosedSpecialDay = SpecialDay.objects.filter(holiday_date = datetime.today().date(), closed=True)
        #ClosedSpecialDay=SpecialDay.objects.get(closed=True)
        #return (datetime.today().date())
        #return ClosedSpecialDay.holiday_date

        dayNo = datetime.today().weekday()

        if dayNo == WEEKDAYS[self.openingDay][0]:
            if not ClosedSpecialDay:
                return WEEKDAYS[self.openingDay][1] + ' ✔'
            else:
                return WEEKDAYS[self.openingDay][1] + ' ❌'
        else:
            return WEEKDAYS[self.openingDay][1]

    def Opening_Hour_starts(self):
        return "{0:0=2d}".format(self.from_hour)+':00'

    def Opening_Hour_ends(self):
        return "{0:0=2d}".format(self.to_hour)+':00'


    def WeekDayToday(self):
        dayNo = datetime.today().weekday()
        if dayNo == WEEKDAYS[self.openingDay][0]:
            return True
        else:
            return False






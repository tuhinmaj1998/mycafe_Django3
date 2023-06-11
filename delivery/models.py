from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe

from order.models import Order
from user.models import UserProfile

class DeliveryLimit(models.Model):
    min_order_to_assign = models.PositiveSmallIntegerField(verbose_name='Min Order to Trigger Schedule')
    maxDistance_1trip_KM = models.IntegerField(verbose_name='Max Distance (KM)  for 1 trip')
    maxWeight_1trip_GRAM = models.IntegerField(verbose_name='Max Weight (Gram)  for 1 trip')
    maxVolume_1trip_CC = models.IntegerField(verbose_name='Max Volume (CC)  for 1 trip')


    class Meta:
        verbose_name = 'Delivery Limit Rule'

    def __str__(self):
        return 'Delivery Rule'

    def title(self):
        return 'Delivery Rule: '



class DeliveryManagement(models.Model):
    STATUS = (
        ('Delivered', 'Delivered'),
        ('Current', 'Current'),
        ('OnShipping', 'OnShipping'),
        ('Ready', 'Ready'),
        ('Waiting', 'Waiting'),
        ('Preparing', 'Preparing'),
        ('Failed', 'Failed'),
    )
    confirmedOrder = models.ForeignKey(Order, on_delete=models.CASCADE)
    deliveryStatus = models.CharField(max_length=100, choices=STATUS, default='Preparing')
    managerNotes = models.CharField(max_length=300, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['confirmedOrder', ]

    def __str__(self):
        return str(str(self.confirmedOrder.id)+' by '+self.confirmedOrder.user.username+' : ')

    def bookingInfo(self):
        return str('Order no. '+str(self.confirmedOrder.id)+' by '+self.confirmedOrder.user.username+' : ')

    def customerUsername(self):
        return self.confirmedOrder.user.username

    def delivery_address(self):
        address = Order.objects.get(id=self.confirmedOrder.id).locationAddress
        return address



#geodjango for location input of order and constantly get delivery boy location
#geosorting based on distance
class DeliveryPartnerProfile(models.Model):
    STATUS = (
        ('Free', 'Free'),
        ('Engaged', 'Engaged'),
        ('Busy', 'Busy'),
    )
    deliveryPartner = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to= Q( groups__name__icontains = 'Delivery-Partner'))
    #deliveryPartnerProfile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},)
    availability = models.BooleanField(default=False)
    pendingDelivery = models.IntegerField(default=0)
    deliveryPartnerStatus = models.CharField(max_length=100, choices=STATUS, default='Free')
    partnerLatitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    partnerLongitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)



    def __str__(self):
        return str(self.deliveryPartner.username)



class DeliveryPartnerSchedule(models.Model):

    deliveryPartner = models.ForeignKey(DeliveryPartnerProfile, on_delete=models.CASCADE)
    readyOrder = models.ForeignKey(DeliveryManagement, on_delete=models.CASCADE)
    #deliveryStatus = models.CharField(max_length=100, choices=STATUS, default='Pending')
    confirmOTP = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-readyOrder', ]

    def __str__(self):
        return str(str(self.readyOrder.id) + ' : by ' + str(self.deliveryPartner))

    def scheduleTime(self):
        management = DeliveryManagement.objects.get(id=self.readyOrder.id)
        return management.timestamp

    def status(self):
        management = DeliveryManagement.objects.get(id=self.readyOrder.id)
        return management.deliveryStatus

    def deliveryPartnerProfile(self):
        partner = UserProfile.objects.get(user_id=self.deliveryPartner.deliveryPartner_id)
        return partner

    def scheduleOrder(self):
        order = Order.objects.get(id=self.readyOrder.confirmedOrder_id)
        return order

    def customerImage(self):
        cImage = UserProfile.objects.get(user_id=self.scheduleOrder().user_id).image
        return cImage

    def delivery_Partner(self):
        partner = UserProfile.objects.get(user_id=self.deliveryPartner.deliveryPartner_id)
        partnerImage = partner.image
        return mark_safe('<img src="{}" height="50px" width="50px" style="border-radius:50%;"/> <br>'.format(partnerImage.url)) + mark_safe(str(self.deliveryPartner))

    def delivery_address(self):
        targetOrder = Order.objects.get(id=self.readyOrder.confirmedOrder_id)
        loc_address = targetOrder.locationAddress
        house_no = targetOrder.houseNo

        if house_no or house_no == '':
            address = house_no + ', '+ loc_address
        else:
            address = loc_address

        return address















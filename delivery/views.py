from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

#from delivery.delivey_schedule import deliverySchedule
from delivery.delivey_schedule import deliveryScheduleRule, deliverySchedule, next_inQueue_schedule
from delivery.group_order import groupOrder
from delivery.models import DeliveryManagement, DeliveryPartnerSchedule, DeliveryPartnerProfile
from order.models import Order, OrderProduct
from user.models import UserProfile

#import delivery.delivey_schedule
def make_ready(request):
    dm = DeliveryManagement.objects.all()
    for everyDm in dm:
        everyDm.deliveryStatus = 'Ready'
        everyDm.save()
    #DeliveryManagement.save()
    dp = DeliveryPartnerProfile.objects.all()
    for everyDp in dp:
        everyDp.deliveryPartnerStatus = 'Free'
        everyDp.save()
    #DeliveryPartnerProfile.save()
    DeliveryPartnerSchedule.objects.all().delete()
    #DeliveryPartnerSchedule.save()

    return HttpResponse('Ready')


def test(request):
    return render(request, 'route.html')

    #return HttpResponse(groupOrder())
    #return HttpResponse(deliveryScheduleRule())


def is_deliveryPartner(request):
    #deliverySchedule(schedule=10)
    current_user = request.user
    if UserProfile.objects.get(user_id=current_user.id).deliveryPartner_status:
        return True

def is_Manager(request):
    current_user = request.user
    if current_user.groups.filter(name__icontains='Manager').exists():
        return True


def forceDelivery(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    checkStatus = is_Manager(request)
    if checkStatus:
        deliverySchedule()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')


def index(request):
    current_user = request.user
    checkStatus = is_Manager(request)
    if checkStatus:

        DeliveryManagements = DeliveryManagement.objects.all().order_by('id')
        ConfirmedOrders = Order.objects.filter(~Q(status='Cancelled'))
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))
        active = 'dashboard'
        userStatus = 'manager'


        context = {'DeliveryManagements': DeliveryManagements, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                   'active': active, 'userStatus': userStatus, }
        return render(request, 'dashIndex.html', context)
    else:
        return HttpResponseRedirect('/')

def OrderPreparingList(request):
    current_user = request.user
    checkStatus = is_Manager(request)
    if checkStatus:

        DeliveryManagements = DeliveryManagement.objects.filter(deliveryStatus='Preparing').order_by('id')
        ConfirmedOrders = Order.objects.filter(~Q(status='Cancelled'))
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))
        active = 'preparing'
        userStatus = 'manager'

        context = {'DeliveryManagements': DeliveryManagements, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                   'active': active, 'userStatus': userStatus, }
        return render(request, 'orderList.html', context)
    else:
        return HttpResponseRedirect('/')

def OrderWaitingList(request):
    current_user = request.user
    checkStatus = is_Manager(request)
    if checkStatus:

        DeliveryManagements = DeliveryManagement.objects.filter(deliveryStatus='Waiting').order_by('id')
        ConfirmedOrders = Order.objects.filter(~Q(status='Cancelled'))
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))
        active = 'waiting'
        userStatus = 'manager'

        context = {'DeliveryManagements': DeliveryManagements, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                   'active': active, 'userStatus': userStatus, }
        return render(request, 'orderList.html', context)
    else:
        return HttpResponseRedirect('/')



def OrderReadyList(request):
    current_user = request.user
    checkStatus = is_Manager(request)
    if checkStatus:

        DeliveryManagements = DeliveryManagement.objects.filter(deliveryStatus='Ready').order_by('id')
        ConfirmedOrders = Order.objects.filter(~Q(status='Cancelled'))
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))
        active = 'ready'
        userStatus = 'manager'

        context = {'DeliveryManagements': DeliveryManagements, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                   'active': active, 'userStatus': userStatus, }
        return render(request, 'orderList.html', context)
    else:
        return HttpResponseRedirect('/')


def finishPreparing(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    checkStatus = is_Manager(request)
    if checkStatus:

        targetOrder = DeliveryManagement.objects.get(id=id)
        targetOrder.deliveryStatus = 'Ready'
        targetOrder.save()

        deliveryScheduleRule()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')


def onShipping(request):
    current_user = request.user
    checkStatus = is_Manager(request)
    if checkStatus:
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))
        schedule = DeliveryPartnerSchedule.objects.all().order_by('readyOrder_id')
        active = 'onShipping'
        userStatus = 'manager'
        context = {'ConfirmedOrderProducts': ConfirmedOrderProducts,
                   'active': active, 'schedule': schedule, 'userStatus': userStatus, }

        return render(request, 'shipment.html', context)
    else:
        return HttpResponseRedirect('/')



def partnerRunningDelivery(request, name):
    current_user = request.user
    checkStatus = is_deliveryPartner(request)
    if checkStatus and name == request.user.username:

        partner = DeliveryPartnerProfile.objects.get(deliveryPartner_id=current_user.id,)
        partnerId = partner.id
        #schedule = DeliveryPartnerSchedule.objects.filter(deliveryPartner_id=partner.id, readyOrder.delivery_status='OnShipping')
        schedule = DeliveryPartnerSchedule.objects.raw('SELECT ds.* FROM delivery_deliveryPartnerSchedule ds JOIN delivery_deliveryManagement dm '
                                                       'ON ds.readyOrder_id = dm.id WHERE dm.deliveryStatus LIKE "OnShipping" and ds.deliveryPartner_id = %s;', [partner.id])
        ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))

        if schedule:
                onShippingSchedule = schedule

                active = 'PartnerOnShipping'
                userStatus = 'partner'

                context = {'onShippingSchedule': onShippingSchedule, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                           'active': active, 'userStatus': userStatus, }
                #return HttpResponse('Yes yes!!! You have')

                return render(request, 'activeScheduled.html', context)

        context={}
        return HttpResponse('No active orders')
    else:
        return HttpResponseRedirect('/')

def partnerCurrentDelivery(request, name):
    current_user = request.user
    checkStatus = is_deliveryPartner(request)
    if checkStatus and name == request.user.username:

        partner = DeliveryPartnerProfile.objects.get(deliveryPartner_id=current_user.id, )
        partnerId = partner.id
        # schedule = DeliveryPartnerSchedule.objects.filter(deliveryPartner_id=partner.id, readyOrder.delivery_status='OnShipping')
        try:
            schedule = DeliveryPartnerSchedule.objects.raw(
                'SELECT ds.* FROM delivery_deliveryPartnerSchedule ds JOIN delivery_deliveryManagement dm '
                'ON ds.readyOrder_id = dm.id WHERE dm.deliveryStatus LIKE "Current" and ds.deliveryPartner_id = %s;',
                [partner.id])
            test = schedule[0]


            ConfirmedOrderProducts = OrderProduct.objects.filter(~Q(status='Cancelled'))

            if schedule:
                currentSchedule = schedule[0]

                active = 'Current'
                userStatus = 'partner'

                delivered = False
                if request.method == 'POST':

                    submit_otp = request.POST.get('otp')
                    o_id = currentSchedule.scheduleOrder().id

                    actual_otp = Order.objects.get(id=o_id).clientOTP
                    if int(submit_otp) == int(actual_otp):
                        d_management = DeliveryManagement.objects.get(id=currentSchedule.readyOrder_id)
                        d_management.deliveryStatus = 'Delivered'
                        d_management.save()

                        targetOrder = currentSchedule.scheduleOrder()
                        targetOrder.status = 'Completed'
                        targetOrder.save()

                        delivered = True

                        next_inQueue_schedule(partnerId)

                        messages.success(request, "Congratulations!!! Your delivery is successful.")
                    else:
                        messages.warning(request, "Please ask customer for correct OTP.")

                context = {'currentSchedule': currentSchedule, 'ConfirmedOrderProducts': ConfirmedOrderProducts,
                           'active': active, 'userStatus': userStatus, 'delivered': delivered, }
                # return HttpResponse('Yes yes!!! You have')

                return render(request, 'activeCurrent.html', context)
        except:
            partner.deliveryPartnerStatus = 'Free'
            partner.save()

            context = {}
            return HttpResponse('No Order is pending')
    else:
        return HttpResponseRedirect('/')



def clickNavigation(request, name, id):
    current_user = request.user
    checkStatus = is_deliveryPartner(request)
    if checkStatus and name == request.user.username:
        address = DeliveryPartnerSchedule.objects.get(id=id).delivery_address()

        address_clean = address.replace(' ', '+')
        print(address_clean)
        url = 'https://www.google.co.in/maps/place/'+address_clean
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect('/')




from django.db.models import Q
from django.http import HttpResponseRedirect

from delivery.group_order import groupOrder
from delivery.models import DeliveryManagement, DeliveryPartnerProfile, DeliveryPartnerSchedule, DeliveryLimit

#import schedule
import time
#from background_task import background

#@background(schedule=60)
def deliverySchedule():
    #url = request.META.get('HTTP_REFERER')
    WaitingOrder = DeliveryManagement.objects.filter(Q(deliveryStatus='Waiting')|Q(deliveryStatus='Ready'))

    groupOrders = []
    groupOrders = groupOrder()

    for everyGrouporders in groupOrders:

        partner = DeliveryPartnerProfile.objects.filter(availability=True, deliveryPartnerStatus='Free')
        if not partner:
            return False

        targetPartner = DeliveryPartnerProfile.objects.get(id=partner[0].id)
        targetPartner.deliveryPartnerStatus = 'Engaged'
        targetPartner.save()

        for every_everyGroupOrders in everyGrouporders:

            schedule = DeliveryPartnerSchedule()
            targetManage = DeliveryManagement.objects.get(confirmedOrder_id = every_everyGroupOrders)

            schedule.readyOrder_id = targetManage.id
            schedule.deliveryPartner_id = partner[0].id
            schedule.save()

            targetManage.deliveryStatus = 'OnShipping'
            targetManage.save()
        deliveryStatus_Current()
    return False

#deliverySchedule(schedule=5, repeat=10,) # 10 seconds from now
#schedule.every(100).seconds.do(deliverySchedule)

#while 1:
#    schedule.run_pending()
#    time.sleep(1)

def deliveryScheduleRule():
    deliveryLimit = DeliveryLimit.objects.filter()[0]
    management = DeliveryManagement.objects.filter(Q(deliveryStatus='Waiting') | Q(deliveryStatus='Ready'))
    print(deliveryLimit.min_order_to_assign)
    print(management.count())

    if deliveryLimit.min_order_to_assign <= management.count():
        deliverySchedule()
        #deliveryStatus_Current()


def deliveryStatus_Current():
    partners = DeliveryPartnerProfile.objects.filter(Q(deliveryPartnerStatus='Engaged'))

    for everyPartner in partners:
        manageId = DeliveryPartnerSchedule.objects.filter(deliveryPartner_id = everyPartner.id).order_by('id')[0].readyOrder_id
        dm = DeliveryManagement.objects.get(id = manageId)
        dm.deliveryStatus = 'Current'
        dm.save()

def next_inQueue_schedule(partnerId):
    onShipping_schedule = DeliveryPartnerSchedule.objects.raw(
            'SELECT ds.* FROM delivery_deliveryPartnerSchedule ds JOIN delivery_deliveryManagement dm '
            'ON ds.readyOrder_id = dm.id WHERE dm.deliveryStatus LIKE "OnShipping" and ds.deliveryPartner_id = %s;',
            [partnerId])
    current_schedule = DeliveryPartnerSchedule.objects.raw(
            'SELECT ds.* FROM delivery_deliveryPartnerSchedule ds JOIN delivery_deliveryManagement dm '
            'ON ds.readyOrder_id = dm.id WHERE dm.deliveryStatus LIKE "Current" and ds.deliveryPartner_id = %s;',
            [partnerId])
    #print('onship', onShipping_schedule[0])
    #print(current_schedule)

    try:
        test = current_schedule[0] #just to check if there is ant current_schedule present
        state = True
    except:
        state = False

    try:

        if onShipping_schedule[0] and state == False:
            onShippingSchedule = onShipping_schedule[0]
            management = DeliveryManagement.objects.get(id = onShippingSchedule.readyOrder_id)
            management.deliveryStatus = 'Current'
            management.save()
    except:
        pass





from math import sqrt
import math
from django.db.models import Q

from delivery.geo_distance import distance
from delivery.models import DeliveryManagement, DeliveryLimit
from order.models import Order





def groupOrder():


    allOrder = []

    management = DeliveryManagement.objects.filter(Q(deliveryStatus='Waiting')|Q(deliveryStatus='Ready'))

    deliveryLimit = DeliveryLimit.objects.filter()[0]

    weightLimit = deliveryLimit.maxWeight_1trip_GRAM

    distanceLimit = deliveryLimit.maxDistance_1trip_KM

    volumeLimit = deliveryLimit.maxVolume_1trip_CC

    for everyManagement in management:
        allOrder.append( Order.objects.get(Q(id=everyManagement.confirmedOrder_id)) )

    allOrderInfo = []

    for everyOrder in allOrder:
        loc = {}
        loc['id']=everyOrder.id
        loc['lat']=float(everyOrder.latitude)
        loc['lng']=float(everyOrder.longitude)
        loc['selected'] = False
        loc['weight'] = int(everyOrder.net_weight_gram())

        allOrderInfo.append(loc)

    #print(allOrderInfo[0]['id'])

    groupOrders = []
    singleGroup = []
    totalWeight = 0
    for everyOrderInfo in allOrderInfo:
        if everyOrderInfo['selected'] == False:

            totalWeight = everyOrderInfo['weight']
            everyOrderInfo['selected'] = True
            singleGroup.append(everyOrderInfo)

            for everyOtherOrderInfo in allOrderInfo:
                if totalWeight <= weightLimit:

                    if everyOrderInfo['id'] != everyOtherOrderInfo['id'] or everyOtherOrderInfo['selected'] == False:
                        dist = distance((everyOrderInfo['lat'], everyOrderInfo['lng']), (everyOtherOrderInfo['lat'], everyOtherOrderInfo['lng']))


                        if dist <distanceLimit and everyOtherOrderInfo['selected'] == False:
                            totalWeight = totalWeight + everyOtherOrderInfo['weight']
                            everyOtherOrderInfo['selected']=True
                            singleGroup.append(everyOtherOrderInfo)

                        else:
                            pass
                else:
                    pass

        if singleGroup:
            res = [sub['id'] for sub in singleGroup]
            groupOrders.append(res)
            singleGroup = []
            print(totalWeight)
            totalWeight = 0

    print(groupOrders)
    return groupOrders










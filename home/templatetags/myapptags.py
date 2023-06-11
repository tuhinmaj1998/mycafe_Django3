from datetime import timedelta

from django import template
from django.db.models import Sum, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from mysite import settings
from offer.models import Subscription_Duration, Fine, ProductDiscount, CashBackCoupon
from order.models import ShopCart, Order
from product.models import Category
from user.models import Subscriber, Wallet, WalletTransaction

register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count


@register.simple_tag
def shopcartAmount(userid):
    totalamount = 0
    userShopCart = ShopCart.objects.filter(user_id=userid)
    for products in userShopCart:
        if products.product.variant == 'None':
            price = products.product.price
        else:
            price = products.variant.price
        quantity = products.quantity
        amount = price*quantity
        totalamount += amount
    return totalamount


@register.simple_tag
def shopcartItems(userid):
    userShopCart = ShopCart.objects.filter(user_id=userid)

    return userShopCart



@register.simple_tag
def checkActiveSubscription(request, userid):
    try:
        activePlan = Subscriber.objects.filter(user_id=request.user.id, status='Active')[0]
        starttime_aware = activePlan.start

        tz_info = starttime_aware.tzinfo
        s_id = activePlan.subcription_id
        plan_info = Subscription_Duration.objects.get(id=s_id)
        totalDuration = plan_info.duration
        activePlan_price = plan_info.price

        startdate = activePlan.start.date()
        enddate = (starttime_aware + timedelta(days=totalDuration)).date()
        # cancelled_date = (starttime_aware + timedelta(days=totalDuration-totalDuration)).date()

        planChange_fine = Fine.objects.get(slug='plan-change').amount

        from django.utils import timezone
        now_aware = timezone.now().date()

        diff = (enddate - now_aware)
        daysRemaining = diff.days
        if daysRemaining > 0:
            moneyRemaining = daysRemaining * (activePlan_price / totalDuration) - (
                    planChange_fine * daysRemaining / totalDuration)
            moneyRemaining = int(float(moneyRemaining))
            subscriptionPeriod = 'Active'
            #activePlan.status = 'Active'



            activePlan.save()
        else:
            moneyRemaining = 0
            activePlan.status = 'Expired'
            activePlan.save()
            subscriptionPeriod = 'Expired'

        sub_dict = {'subscriptionPeriod': subscriptionPeriod, 'moneyRemaining': moneyRemaining,
                    'daysRemaining': daysRemaining}




    except:
        sub_dict = {'subscriptionPeriod': 'Expired', 'moneyRemaining': 0,
                    'daysRemaining': 0}

    return sub_dict

@register.simple_tag
def check_productDiscount_expiry(request):
    discounts = ProductDiscount.objects.filter()
    #print(discounts)

    for everyDiscount in discounts:
        expiry = everyDiscount.expiryDate
        now = timezone.now()
        daysleft = expiry - now
        expiryDay = daysleft.days

        if expiryDay < 0:
            everyDiscount.delete()

    return discounts

    #ProductDiscount.objects.filter(expiryDate__gte = -10, expiryDate__lte = 0).delete()
    #return ProductDiscount.objects.filter()


    #return 'Hi'
    #if expiryDate < 0 and expiryHour < 0:  {% check_productDiscount_expiry request %}
    


@register.simple_tag
def walletInformation(request):
    current_user = request.user

    userWallet = Wallet.objects.get(user_id=current_user.id)
    userWalletTransaction = WalletTransaction.objects.filter(wallet_id=userWallet.id)
    cashBackTransactions = WalletTransaction.objects.filter(Q(wallet_id=userWallet.id) & Q(status='CashBackApplied')|Q(wallet_id=userWallet.id) & Q(status='WalletGift'))

    rewards = 0
    for everyCashBackTransactions in cashBackTransactions:
        reward = everyCashBackTransactions.transactionAmount
        rewards = rewards + reward

    forUserCoupons = CashBackCoupon.objects.filter(Q(user_id=current_user.id)|Q(user_id=None), cashBackTimes__gte=1)
    #forAllCoupons = CashBackCoupon.objects.filter(user_id=None, cashBackTimes__gte=1)



    #activeCoupons = []
    #activeCoupons.append(forUserCoupons)
    #activeCoupons.append(forAllCoupons)
    activeCouponCount = forUserCoupons.count()

    print(forUserCoupons)

    walletInfo = {'userWallet': userWallet, 'userWalletTransaction': userWalletTransaction, 'rewards': rewards,
                  'forUserCoupons': forUserCoupons, 'activeCouponCount': activeCouponCount, }

    return walletInfo



@register.simple_tag
def cashBackRecieved(): #byCoupon

    userOrders = Order.objects.filter(status='Completed', cashBackIssuedStatus=False)

    for everyuserOrder in userOrders:
        cashBack = everyuserOrder.cashBackIssued

        if cashBack != None:
            if cashBack > 0:
                userId = everyuserOrder.user_id

                wallet = Wallet.objects.get(user_id=userId)
                wallet.cashBackTotal = wallet.cashBackTotal + cashBack
                wallet.save()

                everyuserOrder.cashBackIssuedStatus = True
                everyuserOrder.save()

                walletTransaction = WalletTransaction()
                walletTransaction.wallet_id = wallet.id
                walletTransaction.byCashBack = True
                walletTransaction.transactionAmount = everyuserOrder.cashBackIssued
                walletTransaction.cashBackCoupon = everyuserOrder.cashBackCoupon
                walletTransaction.status = 'CashBackApplied'
                walletTransaction.code = get_random_string(10).upper()
                walletTransaction.save()

                #try:
                #    coupon_update = CashBackCoupon.objects.get(code=everyuserOrder.cashBackCoupon)
                #    coupon_update.cashBackTimes = coupon_update.cashBackTimes - 1
                #    coupon_update.save()
                #except:
                #    pass
















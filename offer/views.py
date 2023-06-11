from datetime import timedelta, datetime, date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from offer.models import Subscription, Subscription_Duration, Fine, CashBackCoupon
from order import checksum
from order.models import Order
from user.models import Subscriber, UserProfile, Wallet, WalletTransaction


MERCHANT_KEY = settings.MERCHANT_KEY
MID = settings.MID

def index(request):
    activePlan = Subscriber.objects.filter(user_id = request.user.id, status = 'Active')[0]
    starttime_aware = activePlan.start

    tz_info = starttime_aware.tzinfo
    s_id = activePlan.subcription_id
    plan_info = Subscription_Duration.objects.get(id = s_id)
    totalDuration = plan_info.duration
    activePlan_price = plan_info.price



    startdate = activePlan.start.date()
    enddate = (starttime_aware + timedelta(days=totalDuration)).date()
    #cancelled_date = (starttime_aware + timedelta(days=totalDuration-totalDuration)).date()

    planChange_fine = Fine.objects.get(slug = 'plan-change').amount


    from django.utils import timezone
    now_aware = timezone.now().date()

    diff = (enddate - now_aware)
    daysRemaining = diff.days
    if (daysRemaining > 0 ):
        moneyRemaining = daysRemaining * (activePlan_price / totalDuration) - (planChange_fine * daysRemaining / totalDuration)
        moneyRemaining = int(float(moneyRemaining))
    #return HttpResponse (moneyRemaining)
    else:
        moneyRemaining = 0

    if (daysRemaining == 0):
        plan_info.update(status='Expired')
        k = True
    else:
        k = False


    #return HttpResponse (starttime_aware + timedelta(days=totalDuration))
    #return render(request, 'index.html')
    return HttpResponse(k)



def plans(request):
    current_user = request.user
    plans = Subscription.objects.filter()
    planDuration = Subscription_Duration.objects.filter()

    try:
        subscriber = Subscriber.objects.filter(user_id=current_user.id, status='Active', paid=True).order_by('-start')[0]
        current_plan_durationid = subscriber.subcription_id #say id of bronze (1 month)
        print(current_plan_durationid)
        current_planid = Subscription_Duration.objects.get(id = current_plan_durationid).subscription_id
        print(current_planid)
        current_planrank = Subscription.objects.get(id=current_planid).rank
        current_planprice = Subscription_Duration.objects.get(id=current_plan_durationid).price
        print(current_planrank)
        print(current_planprice)
        context = {'plans': plans, 'planDuration': planDuration, 'subscriber':subscriber,
                   'current_planrank':current_planrank, 'current_planprice': current_planprice, }
    except:
        context = {'plans': plans, 'planDuration': planDuration }


    return render(request, 'plan.html', context)


def individualplan(request, plan, slug):

    current_user = request.user
    plans = Subscription.objects.get(slug = plan)
    selectplanId = plans.id
    planDuration = Subscription_Duration.objects.filter(subscription_id = selectplanId).order_by('-duration')
    select_planDuration = Subscription_Duration.objects.get(slug = slug)
    lowestDayPrice = Subscription_Duration.objects.filter(subscription_id = selectplanId).order_by('price')[0].price
    lowestDay = Subscription_Duration.objects.filter(subscription_id=selectplanId).order_by('duration')[0].duration
    highestPricePerDay = float(lowestDayPrice / lowestDay)
    print(highestPricePerDay)
    from django.utils import timezone
    now_aware = timezone.now()
    end_aware = (now_aware + timedelta(days=select_planDuration.duration)).date()
    now_aware = timezone.now().date()

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
        if (daysRemaining > 0):
            moneyRemaining = daysRemaining * (activePlan_price / totalDuration) - (
                    planChange_fine * daysRemaining / totalDuration)
            moneyRemaining = int(float(moneyRemaining))

            usage_charge = int(planChange_fine * daysRemaining / totalDuration)
        else:
            moneyRemaining = 0

            usage_charge = 0



        subscriber = Subscriber.objects.filter(user_id=current_user.id, status='Active', paid=True).order_by('-start')[0]
        current_plan_durationid = subscriber.subcription_id  # say id of bronze (1 month)
        print(current_plan_durationid)
        current_planid = Subscription_Duration.objects.get(id=current_plan_durationid).subscription_id
        print(current_planid)
        current_planrank = Subscription.objects.get(id=current_planid).rank
        current_planprice = Subscription_Duration.objects.get(id=current_plan_durationid).price
        current_planname = Subscription_Duration.objects.get(id=current_plan_durationid).title
        print(current_planrank)
        print(current_planprice)
        context = {'plans': plans, 'planDuration': planDuration, 'subscriber': subscriber,
                   'current_planrank': current_planrank, 'highestPricePerDay':highestPricePerDay,
                   'select_planDuration': select_planDuration, 'now_aware': now_aware, 'end_aware': end_aware,
                   'current_planprice': current_planprice,
                   'startdate': startdate, 'enddate': enddate, 'daysRemaining': daysRemaining,
                   'moneyRemaining': moneyRemaining, 'current_planname': current_planname,
                   'usage_charge': usage_charge, 'activePlan_price': activePlan_price, 'totalDuration': totalDuration,
                   'diff': diff, }
    except:
        context = {'plans': plans, 'planDuration': planDuration, 'highestPricePerDay':highestPricePerDay,
                   'select_planDuration': select_planDuration, 'now_aware': now_aware, 'end_aware': end_aware,}

    return render(request, 'individualPlan.html', context)



@login_required(login_url='/login') # Check login
def purchaseplan(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    ordercode = get_random_string(10).upper()


    try:
        activePlan = Subscriber.objects.get(user_id=request.user.id, status='Active')
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
        else:
            moneyRemaining = 0

    except:
        moneyRemaining = 0

    if request.method == 'POST':
        data = Subscriber()
        data.subcription_id = id
        data.user_id = current_user.id
        data.ip = request.META.get('REMOTE_ADDR')
        data.code = ordercode
        #data.userEnds = None
        data.save()
        total = Subscription_Duration.objects.get(id = id).price - moneyRemaining

        name = request.user.get_username()
        print('username is: ', name)
        # name='tuhin'
        param_dict = {
            'MID': MID,
            'ORDER_ID': str(ordercode),
            'TXN_AMOUNT': str(total),
            'CUST_ID': str(UserProfile.objects.get(user_id=current_user.id).user.email),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/offer/handleRequest/' + name,
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)

        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'total': total,
                   'profile': profile,
                   'param_dict': param_dict,
                   }
        return render(request, 'paytm.html', context)

    plans = Subscription.objects.filter()
    planDuration = Subscription_Duration.objects.filter()
    subscriber = Subscriber.objects.filter(user_id = current_user.id, status = 'Active')[0]
    context = {'plans': plans, 'planDuration': planDuration, 'subscriber':subscriber}
    return HttpResponseRedirect(url)
    #return render(request, 'plan.html', context)

@csrf_exempt
def handleRequest(request, user):

    user = User.objects.get(username=user)
    # manually set the backend attribute
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    current_user = request.user
    userProfile = UserProfile.objects.get(user_id=current_user.id)
    request.session['userimage'] = userProfile.image.url
    user_name = request.user.get_full_name()

    print(user)
    form = request.POST
    checksum_response = 0
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum_response = form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum_response)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successful')
            # uid = Order.objects.filter(code = str(response_dict['ORDERID']))
            # print (uid.get(pk=1))

            try:
                activePlan = Subscriber.objects.get(user_id=request.user.id, status='Active')
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
                    activePlan.update(userEnds=(datetime.now()))
                    activePlan.update(status='Cancelled')
                    print('Working')


                elif daysRemaining == 0:

                    activePlan.update(userEnds=(datetime.now()))
                    activePlan.update(status='Expired')

            except:
                daysRemaining = 0


            #from django.utils import timezone
            #now_aware = timezone.now().date()



            order_update = Subscriber.objects.get(code=response_dict['ORDERID'])
            order_update.status = 'Active'
            order_update.paid = True
            order_update.TXNID = response_dict['TXNID']
            order_update.TXNAMOUNT = response_dict['TXNAMOUNT']
            order_update.TXNDATE = response_dict['TXNDATE']
            order_update.GATEWAYNAME = response_dict['GATEWAYNAME']
            order_update.BANKTXNID = response_dict['BANKTXNID']
            order_update.BANKNAME = response_dict['BANKNAME']

            # order_update.refresh_from_db(fields=['status'])
            Subscriber.save(self=order_update)
            # print(order_update.status)

            current_user = request.user  # Access User Session information
            # Order.objects.filter(user_id=current_user.id, code= ).delete()
            messages.success(request, "Congratulations. You are now prime member.")
        else:
            messages.warning(request, "Your Payment is not successful. Please try again.")
            print('Payment was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'paymentstatusSubscription.html', {'response': response_dict,
                                                  'user_name': user_name})

def checkValidCoupon(request):
    current_user = request.user
    url = request.META.get('HTTP_REFERER')
    textCode = request.GET.get('couponCode')


    if textCode == None or textCode=='':
        return None

    else:
        textCode = request.GET.get('couponCode').upper().strip()
        #print(textCode)

        try:
            codesForAll = CashBackCoupon.objects.get(user_id=None, code=textCode,)
            print('codesForAll', codesForAll)
        except:
            codesForAll = False
            pass
        try:
            codesForUser = CashBackCoupon.objects.get(user_id=current_user.id, code=textCode)
            print('codesForUser', codesForUser)
        except:
            codesForUser = False
            pass

        if codesForAll or codesForUser:


            if codesForAll:
                expiry = codesForAll.cashBackexpiryDate
                now = timezone.now()
                CBdaysleft = expiry - now

                #userWallet = Wallet.objects.get(user_id=current_user.id)
                #userWalletTransaction = WalletTransaction.objects.filter(wallet_id=userWallet.id, cashBackCoupon=textCode)
                couponUseOrNot = Order.objects.filter(Q(user_id=current_user.id) & Q( cashBackCoupon=textCode) & ~Q(status='Cancelled'))

                print(couponUseOrNot)

                if CBdaysleft.days >= 0:
                    if codesForAll.cashBackTimes == 0 or len(couponUseOrNot) > 0:
                        messages.error(request, 'Oops!!! Limit is exceeded for this coupon.')
                        return 'Limit Exceeded'
                    else:
                        messages.success(request, 'Congratulations!!! PromoCode Applied.')
                        return codesForAll
                else:
                    messages.warning(request, 'Sorry!!! Coupon code is expired.')
                    return 'expired'

            else:
                expiry = codesForUser.cashBackexpiryDate
                now = timezone.now()
                CBdaysleft = expiry - now
                if CBdaysleft.days >= 0:
                    if codesForUser.cashBackTimes == 0:
                        messages.error(request, 'Oops!!! Limit is exceeded for this coupon.')
                        return 'Limit Exceeded'
                    else:
                        messages.success(request, 'Congratulations!!! PromoCode Applied.')
                        return codesForUser
                else:
                    messages.warning(request, 'Sorry!!! Coupon code is expired.')
                    return 'expired'

        else:
            messages.warning(request,'This is not a valid coupon code.')
            return False



        #return render(request,'Order_form.html', )
        #return HttpResponseRedirect(url)


def applyWallet(request):
    current_user = request.user
    try:
        userWallet = Wallet.objects.get(user_id = current_user.id)
    except:
        makeWallet = Wallet()
        makeWallet.user_id = current_user.id
        makeWallet.save()
        userWallet = Wallet.objects.get(user_id=current_user.id)

    return userWallet


def cashBackRecieved(request): #byCoupon
    current_user = request.user
    userOrder = Order.objects.filter(user_id=current_user.id, status='Completed', cashBackIssuedStatus=False)
    wallet = Wallet.objects.get(user_id=current_user.id)
    walletTransaction = WalletTransaction()

    for everyuserOrder in userOrder:
        if everyuserOrder.cashBackIssued > 0:
            wallet.cashBackTotal = wallet.cashBackTotal + everyuserOrder.cashBackIssued
            wallet.save()

            everyuserOrder.cashBackIssuedStatus = True
            everyuserOrder.save()

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








def walletDeduction(request, code):
    current_user = request.user
    order_update = Order.objects.get(code=code, user_id=current_user.id, walletDeductionStatus=False)

    wallet = Wallet.objects.get(user_id=current_user.id)

    if order_update.walletDeduction > 0:
        wallet.cashBackTotal = wallet.cashBackTotal - order_update.walletDeduction
        wallet.save()
        order_update.walletDeductionStatus = True
        order_update.save()

        print('wallet transaction is: ', order_update.walletDeduction)

        walletTransactions = WalletTransaction()
        walletTransactions.wallet_id = wallet.id
        walletTransactions.transactionAmount = order_update.walletDeduction
        walletTransactions.status = 'Paid'
        walletTransactions.code = get_random_string(10).upper()
        walletTransactions.timeIssued = datetime.now()

        walletTransactions.save()

        try:
            coupon_update = CashBackCoupon.objects.get(code=order_update.cashBackCoupon)
            coupon_update.cashBackTimes = coupon_update.cashBackTimes - 1
            coupon_update.save()
        except:
            pass















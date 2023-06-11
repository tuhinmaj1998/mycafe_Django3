import random
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, load_backend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from delivery.models import DeliveryManagement
from offer.models import Subscription_Duration, Fine, ProductDiscount, CashBackCoupon
from order import checksum
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Variants
from user.models import UserProfile, Subscriber, Wallet, UserAddress


def index(request):
    return HttpResponse ('Order Page')


@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)



    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        variantid = request.POST.get('variantid')
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity = form.cleaned_data['quantity']

                data.save()  # save data
            else : # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                print('Yes reached')
                data.save()
            messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            if product.variant == 'None':
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            else:
                v = Variants.objects.get(product_id=id, price = product.price)

                try:
                    data = ShopCart.objects.get(user_id=current_user.id, product_id=id, variant_id=v.id)
                except:
                    data = ShopCart()  # model ile bağlantı kur
                    data.user_id = current_user.id
                    data.product_id = id
                    data.quantity = 0
                    v = Variants.objects.get(product_id=id, price=product.price)
                    data.variant_id = v.id

            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            if product.variant == 'None':

                data.variant_id =None
            else:
                v = Variants.objects.get(product_id=id, price = product.price)
                data.variant_id = v.id

            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):

    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total = 0
    discountlessTotal = 0
    discountOff = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            try:
                disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                actualPrice = rs.product.price
                nowPrice = actualPrice - actualPrice * disP.discountPercent / 100
                print(disP, nowPrice)

            except:
                actualPrice = rs.product.price
                nowPrice = actualPrice

            total += nowPrice * rs.quantity
            discountlessTotal += actualPrice * rs.quantity
        else:
            try:
                disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                actualPrice = rs.variant.price
                nowPrice = actualPrice - actualPrice * disP.discountPercent / 100
                print(disP, nowPrice)
            except:
                actualPrice = rs.variant.price
                nowPrice = actualPrice

            total += nowPrice * rs.quantity
            discountlessTotal += rs.variant.price * rs.quantity
            #print(total)

    try:
        activePlan = Subscriber.objects.filter(user_id=request.user.id, status='Active')[0]
        s_id = activePlan.subcription_id
        plan_info = Subscription_Duration.objects.get(id=s_id)
        limit_amount = plan_info.limit_amount
        percentage = plan_info.percentage

        if total * percentage/100 > limit_amount:
            totalprice = total - limit_amount
            priceOff = limit_amount
        else:
            totalprice = total - total*percentage/100
            priceOff = total*percentage/100



    except:
        totalprice = total
        priceOff = 0


    #return HttpResponse(str(total))
    context={'shopcart': shopcart,'total': total, 'discountlessTotal': discountlessTotal,
             'totalprice':totalprice, 'priceOff': priceOff, }
    return render(request,'shopcart_products.html',context)

@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item is removed form Shopcart.")
    #return HttpResponseRedirect("/shopcart")
    return HttpResponseRedirect(url)



MERCHANT_KEY = settings.MERCHANT_KEY
MID = settings.MID

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login') # Check login
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    userAddress = UserAddress.objects.filter(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    ordercode = get_random_string(10).upper()

    couponInfo = []
    from offer.views import checkValidCoupon
    couponInfo = checkValidCoupon(request)



    from offer.views import applyWallet
    applyWalletInfo = applyWallet(request)





    total = 0
    discountlessTotal = 0
    discountOff = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            try:
                disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                actualPrice = rs.product.price
                nowPrice = actualPrice - actualPrice * disP.discountPercent / 100
                print(disP, nowPrice)
            except:
                actualPrice = rs.product.price
                nowPrice = actualPrice

            total += nowPrice * rs.quantity
            discountlessTotal += actualPrice * rs.quantity
        else:
            try:
                disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                actualPrice = rs.variant.price
                nowPrice = actualPrice - actualPrice * disP.discountPercent / 100
                print(disP, nowPrice)
            except:
                actualPrice = rs.variant.price
                nowPrice = actualPrice

            total += nowPrice * rs.quantity
            discountlessTotal += rs.variant.price * rs.quantity


    #check user has subscribed to any plan or not. priceOff is the amount subtract from original price.
    try:
        activePlan = Subscriber.objects.filter(user_id=request.user.id, status='Active')[0]
        s_id = activePlan.subcription_id
        plan_info = Subscription_Duration.objects.get(id=s_id)
        limit_amount = plan_info.limit_amount
        percentage = plan_info.percentage

        if total * percentage/100 > limit_amount:
            totalprice = total - limit_amount
            priceOff = limit_amount
        else:
            totalprice = total - total*percentage/100
            priceOff = total*percentage/100



    except:
        totalprice = total
        priceOff = 0

    if request.method == 'POST':  # if there is a post


        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            #data.address = form.cleaned_data['address']
            #data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.locationAddress = form.cleaned_data['locationAddress']
            data.houseNo = form.cleaned_data['houseNo']
            data.latitude = form.cleaned_data['latitude']
            data.longitude = form.cleaned_data['longitude']

            print(form.cleaned_data['useWallet'])
            data.useWallet = form.cleaned_data['useWallet']
            data.user_id = current_user.id



            data.total = total
            data.priceOffPlan = total - totalprice
            data.discountOff = discountlessTotal - total

            walletMoneyDeducted = 0

            if form.cleaned_data['useWallet']:
                walletMoneyDeducted = applyWalletInfo.cashBackTotal
                if(totalprice <= walletMoneyDeducted):
                    walletMoneyDeducted = totalprice
                else:
                    walletMoneyDeducted = applyWalletInfo.cashBackTotal

            paybleAmount = float(totalprice) - float(walletMoneyDeducted)
            paybleAmount = round(paybleAmount, 2)
            data.walletDeduction = walletMoneyDeducted



            try:
                print(couponInfo.code)
                cashBackAdded = total * couponInfo.cashBackPercent / 100
                if cashBackAdded >= couponInfo.cashBackLimit:
                    cashBackAdded = couponInfo.cashBackLimit
                data.cashBackIssued = cashBackAdded
                data.cashBackCoupon = couponInfo.code

            except:
                pass



            data.ip = request.META.get('REMOTE_ADDR')
            # random code
            data.code = ordercode
            data.save()  #

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                    productDiscountOff = 0
                    try:
                        disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                        actualPrice = rs.product.price

                        detail.productDiscountOff = actualPrice * disP.discountPercent / 100
                    except:
                        #actualPrice = rs.product.price
                        detail.productDiscountOff = 0
                else:
                    detail.price = rs.variant.price
                    try:
                        disP = ProductDiscount.objects.get(product_id=rs.product.id, variant_id=rs.variant_id)
                        actualPrice = rs.variant.price

                        detail.productDiscountOff = actualPrice * disP.discountPercent / 100
                    except:
                        # actualPrice = rs.product.price
                        detail.productDiscountOff = 0
                detail.variant_id = rs.variant_id
                detail.amount = detail.quantity * detail.price
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if rs.product.variant == 'None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.variant_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                #************ <> *****************
            name = request.user.get_username()
            print('username is: ', name)


            #name='tuhin'
            param_dict = {
                'MID': MID,
                'ORDER_ID': str(ordercode),
                'TXN_AMOUNT': str(paybleAmount),
                'CUST_ID': str( UserProfile.objects.get(user_id=current_user.id).user.email),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/order/handleRequest/'+ name,
            }


            if(paybleAmount==0 and totalprice > 0):
                print('Order Successful')
                # uid = Order.objects.filter(code = str(response_dict['ORDERID']))
                # print (uid.get(pk=1))

                order_update = Order.objects.get(code=ordercode, user_id=current_user.id)
                order_update.status = 'Accepted'
                order_update.paid = True

                order_update.clientOTP = random.randint(1111, 9999)

                # order_update.useWallet = True
                # order_update.refresh_from_db(fields=['status'])
                Order.save(self=order_update)

                from offer.views import walletDeduction
                walletDeduction(request, ordercode)
                # print(order_update.status)

                entryDeliveryManagemant = DeliveryManagement()
                entryDeliveryManagemant.confirmedOrder_id = order_update.id
                entryDeliveryManagemant.save()

                current_user = request.user  # Access User Session information
                ShopCart.objects.filter(user_id=current_user.id).delete()
                request.session['cart_items'] = 0
                # Order.objects.filter(user_id=current_user.id, code= ).delete()
                messages.success(request, "Your Order has been completed. Thank you ")

                return HttpResponseRedirect('http://127.0.0.1:8000/order/handleRequest/'+ name)




            else:
                param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)

                form = OrderForm()
                profile = UserProfile.objects.get(user_id=current_user.id)
                context = {'shopcart': shopcart,  'total': total, 'totalprice': totalprice, 'discountlessTotal': discountlessTotal,
                           'form': form, 'profile': profile, 'param_dict': param_dict, 'priceOff': priceOff, 'couponInfo': couponInfo,
                           'applyWalletInfo': applyWalletInfo, 'userAddress': userAddress,
                           }
                return render(request, 'paytm.html', context)


    context2 = {'shopcart': shopcart, 'total': total, 'totalprice': totalprice, 'discountlessTotal': discountlessTotal,
                'profile': UserProfile.objects.get(user_id=current_user.id), 'priceOff': priceOff,
                'couponInfo': couponInfo,
                'applyWalletInfo': applyWalletInfo, 'userAddress': userAddress,
                }

    return render(request, 'Order_Form.html', context2)
        #else:
         ##  return HttpResponseRedirect("/order/orderproduct")



    #return render(request, 'Order_Form.html', context)
@csrf_exempt
def handleRequest(request, user):
    category = Category.objects.all()
    #username = 'tuhin'
    user = User.objects.get(username=user)
    # manually set the backend attribute
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    current_user = request.user
    userProfile = UserProfile.objects.get(user_id=current_user.id)
    request.session['userimage'] = userProfile.image.url
    user_name = request.user.get_full_name()

    try:
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
                #uid = Order.objects.filter(code = str(response_dict['ORDERID']))
                #print (uid.get(pk=1))

                order_update = Order.objects.get(code=response_dict['ORDERID'], user_id=current_user.id)
                order_update.status = 'Accepted'
                order_update.paid = True

                #order_update.useWallet = True
                order_update.TXNID = response_dict['TXNID']
                order_update.TXNDATE = response_dict['TXNDATE']
                order_update.GATEWAYNAME = response_dict['GATEWAYNAME']
                order_update.BANKTXNID = response_dict['BANKTXNID']
                order_update.BANKNAME = response_dict['BANKNAME']

                order_update.clientOTP = random.randint(1111, 9999)
                Order.save(self=order_update)

                from offer.views import walletDeduction
                walletDeduction(request, response_dict['ORDERID'])
                #print(order_update.status)

                entryDeliveryManagemant = DeliveryManagement()
                entryDeliveryManagemant.confirmedOrder_id = order_update.id
                entryDeliveryManagemant.save()



                current_user = request.user  # Access User Session information
                ShopCart.objects.filter(user_id=current_user.id).delete()
                request.session['cart_items'] = 0
                #Order.objects.filter(user_id=current_user.id, code= ).delete()
                messages.success(request, "Your Order has been completed. Thank you ")
            else:
                order_update = Order.objects.get(code=response_dict['ORDERID'])
                order_update.useWallet = False
                order_update.walletDeduction = 0.00
                Order.save(self=order_update)





                messages.warning(request, "Your Order is not received. Please try again. ")
                print('Order was not successful because ' + response_dict['RESPMSG'])
        return render(request, 'paymentstatus.html', {'response': response_dict,
                                                      'category': category,
                                                      'user_name': user_name})
    except:
        return render(request, 'paymentstatus.html', {'user_name': user_name})
        



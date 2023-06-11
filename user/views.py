from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from offer.models import Fine
from order import checksum
from order.models import Order, OrderProduct
from product.models import Category, Comment, Reply
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile, WalletTransaction, Wallet, WalletForm, UserAddress


@login_required(login_url='/login') # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category, 'active': 'user',
               'profile':profile}
    return render(request,'user_profile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_form(request):
    category = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userProfile  = UserProfile.objects.get(user_id = current_user.id)
            request.session['userimage'] = userProfile.image.url
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Error. Username or Password is incorrect")
            return HttpResponseRedirect('/login')
        # Return an 'invalid login' error message.

    context = {   'category': category
    }
    return render(request, 'login_form.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.webp"
            data.save()
            current_user = request.user
            userProfile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userProfile.image.url
            messages.success(request, 'Your account has been created!')
            makeWallet = Wallet()
            makeWallet.user_id = current_user.id
            makeWallet.save()

            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Category.objects.all()
    context = {   'category': category,
                  'form': form,}
    return render(request, 'signup_form.html', context)


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form, 'active': 'user_update',
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'category': category, 'active': 'passwords'})


@login_required(login_url='/login') # Check login
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'orders': orders, 'active': 'orders'
               }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems, 'active': 'orderdetail'
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login') # Check login
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems, 'active': 'order_product'
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments, 'active': 'comments'
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    check = Comment.objects.filter(id=id, user_id=current_user.id)
    if check:
        messages.success(request, 'Comment deleted..')
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.warning(request, 'Something went wrong')

    return HttpResponseRedirect(url)

@login_required(login_url='/login') # Check login
def user_deletereply(request, id, cid):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    check = Reply.objects.filter(id=id, user_id=current_user.id, parentComment_id=cid)
    if check:
        messages.success(request, 'Reply is deleted..')
    Reply.objects.filter(id=id, user_id=current_user.id, parentComment_id=cid).delete()
    messages.warning(request, 'Something went wrong')

    return HttpResponseRedirect(url)



@login_required(login_url='/login') # Check login
def user_wallet(request):
    #url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    userWallet = Wallet.objects.get(user_id=current_user.id)
    userWalletTransaction = WalletTransaction.objects.filter(wallet_id=userWallet.id).order_by('-timeIssued')

    context = {'userWalletTransaction': userWalletTransaction, 'active': 'wallet'}

    return render(request, 'wallet.html', context)


MERCHANT_KEY = 'VMHLjjUs1VBsq61!'
@login_required(login_url='/login') # Check login
def addMoneyToWallet(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    ordercode = get_random_string(10).upper()
    user_wallet = Wallet.objects.get(user_id=current_user.id)


    if request.method == 'POST':
        form = WalletForm(request.POST)
        # return HttpResponse(request.POST.items())
        data = WalletTransaction()
        if form.is_valid():
            data.transactionAmount = form.cleaned_data['transactionAmount']

            data.wallet_id = user_wallet.id
            data.ip = request.META.get('REMOTE_ADDR')

            data.code = ordercode
            # data.userEnds = None
            data.save()
            total = data.transactionAmount
            print(total)
            name = request.user.get_username()
            print('username is: ', name)
            # name='tuhin'
            param_dict = {
                'MID': 'ijzpqJ66315450163074',
                'ORDER_ID': str(ordercode),
                'TXN_AMOUNT': str(total),
                'CUST_ID': str(UserProfile.objects.get(user_id=current_user.id).user.email),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/user/wallet/handleRequest/' + name,
            }
            param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)

            profile = UserProfile.objects.get(user_id=current_user.id)
            context = {'total': total,
                       'profile': profile,
                       'param_dict': param_dict,
                       }
            return render(request, 'paytm.html', context)


    context = {}
    return HttpResponseRedirect(url)
    # return render(request, 'plan.html', context)

@csrf_exempt
def walletHandleRequest(request, user):
    user = User.objects.get(username=user)
    # manually set the backend attribute
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    current_user = request.user
    userProfile = UserProfile.objects.get(user_id=current_user.id)
    request.session['userimage'] = userProfile.image.url
    user_name = request.user.get_full_name()

    #print(user)
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



            userWallet = Wallet.objects.get(user_id=user.id)
            print(userWallet)
            userWalletid = userWallet.id
            userWalletTransaction = WalletTransaction.objects.get(code=response_dict['ORDERID'], wallet_id=userWalletid)

            if userWalletTransaction.paid == False:
                userWalletTransaction.wallet_id = userWalletid
                userWalletTransaction.status = 'Received'
                userWalletTransaction.paid = True
                userWalletTransaction.TXNID = response_dict['TXNID']
                userWalletTransaction.TXNAMOUNT = response_dict['TXNAMOUNT']
                userWalletTransaction.TXNDATE = response_dict['TXNDATE']
                userWalletTransaction.GATEWAYNAME = response_dict['GATEWAYNAME']
                userWalletTransaction.BANKTXNID = response_dict['BANKTXNID']
                userWalletTransaction.BANKNAME = response_dict['BANKNAME']

                # order_update.refresh_from_db(fields=['status'])
                WalletTransaction.save(self=userWalletTransaction)

                extraAdd = 0.0
                extraAmountTransaction = WalletTransaction()
                if extraAmountTransaction.walletGiftStatus == False:
                    extraAmountTransaction.wallet_id = userWalletid
                    extraAmountTransaction.status = 'WalletGift'
                    giftFine = Fine.objects.get(slug = 'wallet-add-gift')
                    percentageAdd = giftFine.percentage
                    extraAmountTransaction.transactionAmount = float(response_dict['TXNAMOUNT']) * float(percentageAdd) / 100.00
                    extraAmountTransaction.walletGiftStatus=True
                    extraAmountTransaction.code = get_random_string(10).upper()
                    extraAdd = extraAmountTransaction.transactionAmount
                    extraAmountTransaction.save()




                    userWallet.cashBackTotal = userWallet.cashBackTotal + float(response_dict['TXNAMOUNT']) + float(extraAdd)
                    userWallet.save()



            current_user = request.user  # Access User Session information
            # Order.objects.filter(user_id=current_user.id, code= ).delete()
            messages.success(request, "Congratulations!!! Wallet Amount has been added.")
        else:
            messages.warning(request, "Your Payment is not successful. Please try again.")
            print('Payment was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'paymentstatusWallet.html', {'response': response_dict,
                                                              'user_name': user_name})







def userAddress(request):
    current_user = request.user
    userAddress = UserAddress.objects.filter(user_id=current_user.id)



    context = {'userAddress': userAddress, 'active': 'address', }
    return render(request, 'userAddress.html', context)



def addNewAddress(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    if request.method == 'POST':
        addAddress = UserAddress()
        addAddress.user_id = current_user.id
        addAddress.locationAddress = request.POST['locationAddress']
        addAddress.latitude = request.POST['latitude']
        addAddress.longitude = request.POST['longitude']
        addAddress.title = request.POST['title']
        addAddress.description = request.POST['description']

        import random
        import colorsys
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

        color = '#%02x%02x%02x' % (r, g, b)

        addAddress.color = color
        addAddress.save()
        next = request.POST['path']
        return HttpResponseRedirect(next)
        #return HttpResponseRedirect('address/')



    return render(request, 'addNewAddress.html')






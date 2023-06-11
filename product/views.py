from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from order.models import ShopCart
from product.models import CommentForm, Comment, Product, WishList, WishListForm, Variants, ReplyForm, Reply


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("<h1>Hello Django</h1>")

def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your review.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


def addreply(request, id, cid):
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = ReplyForm(request.POST)
        if form.is_valid():
            data = Reply()  # create relation with model
            data.reply = form.cleaned_data['reply']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            data.parentComment_id = cid
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Thank you for your reply.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


def colors(request):
    return render(request,'product_color.html')


@login_required(login_url='/login') # Check login
def addtowishlist(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = WishList.objects.filter(variant_id=variantid,
                                                 user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        variantid = request.POST.get('variantid')
        checkinproduct = WishList.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = WishListForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  WishList
                if product.variant == 'None':
                    data = WishList.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = WishList.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.checked = not form.cleaned_data['checked']
                data.save()  # save data
                messages.warning(request, "Product is removed from My Wish List")
            else:  # Inser to WishList
                data = WishList()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.checked = form.cleaned_data['checked']
                data.save()
                messages.success(request, "Product added to My Wish List")
        WishList.objects.filter(checked=False).delete()
        try:
            return HttpResponseRedirect(url)
        except:
            return HttpResponse("working")

    else:  # if there is no post
        if control == 1:  # Update  WishList
            if product.variant == 'None':
                data = WishList.objects.get(product_id=id, user_id=current_user.id)
                data.checked = False
            else:
                v = Variants.objects.get(product_id=id, price=product.price)

                try:
                    data = WishList.objects.get(user_id=current_user.id, product_id=id, variant_id=v.id)
                    data.checked = False
                except:
                    data = WishList()
                    data.user_id = current_user.id
                    data.product_id = id
                    data.checked = True
                    v = Variants.objects.get(product_id=id, price=product.price)
                    data.variant_id = v.id


            data.save()  #
        else:  # Insert to Shopcart
            data = WishList()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.checked = True
            if product.variant == 'None':

                data.variant_id = None
            else:
                v = Variants.objects.get(product_id=id, price=product.price)
                data.variant_id = v.id

            data.save()  #

        messages.success(request, "Product added to My Wish List")
        WishList.objects.filter(checked=False).delete()


        return HttpResponseRedirect(url)


@login_required(login_url='/login') # Check login
def wishlist(request):
    current_user = request.user  # Access User Session information
    wishlist = WishList.objects.filter(user_id=current_user.id)
    myshopcart = ShopCart.objects.filter(user_id=current_user.id)
    context = {'wishlist': wishlist,
               'myshopcart' : myshopcart, 'active': 'favourites'
               }
    return render(request, 'wishlist.html', context)



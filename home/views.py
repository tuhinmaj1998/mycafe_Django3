import json

from django.conf import Settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from collections import OrderedDict
import pandas as pd

# Create your views here.
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage, FAQ
from offer.models import ProductDiscount
from order.models import ShopCart
from product.models import Category, Product, Images, Comment, Variants, GoesWellWith, WishList, SearchHistory, Reply
from user.models import UserProfile


def sendEmail(request):
    userEmail = request.user.email
    #send_mail('Hello, Welcome to Cafe bro homepage',
    #          'Thank you for visiting our page. Please support us!!!',
    #          'Cafe Bro', [userEmail],
    #          fail_silently=False)

    html_content = render_to_string("Email_template.html", {'title': 'Thanks for Registering!', 'name': request.user.user_name})
    text_content = strip_tags(html_content)



    email = EmailMultiAlternatives(
        'testing', text_content, 'donotreply@cafebro.com', [userEmail])
    email.attach_alternative(html_content, "text/html")
    email.send()

    return HttpResponse('Sent to '+ userEmail)



def index(request):
    current_user = request.user  # Access User Session information
    setting = Setting.objects.get(pk=1)

    #category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:3]# first 3 products
    products_latest = Product.objects.all().order_by('-id')[:8]# last 8 products
    products_coffee = Product.objects.filter(keywords__contains='coffee')# status true
    products_picked = Product.objects.all().order_by('?')[:8]# random 8 products
    page = "home"

    wishlist = WishList.objects.filter(user_id=current_user.id)
    topwish = WishList.objects.raw('select w.*, count(w.product_id) as times from product_wishlist w group by w.product_id order by times desc;')

    countWish = wishlist.count()
    #print('count wishlist is:', countWish)
    myshopcart = ShopCart.objects.filter(user_id=current_user.id)
    variant = Variants.objects.all()

    discountP = ProductDiscount.objects.all()
    print(topwish)



    context = {'setting' : setting, 'page':page, 'products_slider': products_slider, 'products_latest': products_latest,
               'products_coffee': products_coffee, 'products_random': products_picked, 'wishlist':wishlist, 'myshopcart': myshopcart,
               'variant': variant,'n': 'False', 'discountP': discountP, 'countWish': countWish, 'topwish':topwish,}
    return render(request, 'index.html', context)
    #return HttpResponse("<h1>Hello Django</h1>")

def aboutus(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting' : setting,  'category':category}
    return render(request, 'aboutus.html', context)


def contact(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form, 'category':category}
    return render(request, 'contact.html', context)

def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'setting' : setting,
               'category': category,
               'products': products, }
    return render(request, 'category_products.html', context)
    #return HttpResponse(products)

def product_detail(request, id, slug):


    query = request.GET.get('q')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True').order_by('-create_at')
    goeswellwith = GoesWellWith.objects.filter(product=product)
    reply = Reply.objects.filter(status = 'True').order_by('-create_at')
    ownprofile = UserProfile.objects.filter()


    current_user = request.user  # Access User Session information

    context = {'setting' : setting, 'category': category, 'product': product,'images':images,
               'comments': comments, 'goeswellwith':goeswellwith, 'reply': reply,'ownprofile':ownprofile,}

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
            try:
                shopcart = ShopCart.objects.get(user_id=current_user.id, product_id=id, variant=variant_id)
            except:
                shopcart = 0
            try:
                wishlist = WishList.objects.get(user_id=current_user.id, product_id=id, variant=variant_id)
                wcheck = wishlist.checked
                #print(wcheck)
            except:
                wishlist = 0
                wcheck = False
                #wcheck = wishlist['checked']
                #print(wcheck)
            try:
                proDis = ProductDiscount.objects.get(product_id=id, variant=variant_id)

            except:
                proDis = 0


        else:
            #variant_id = request.POST.get('variantid')
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
            try:
                shopcart = ShopCart.objects.get(user_id=current_user.id, product_id=id, variant=variants[0])
            except:
                shopcart = 0

            try:
                wishlist = WishList.objects.get(user_id=current_user.id, product_id=id, variant=variants[0])
            except:
                wishlist = 0

            try:
                proDis = ProductDiscount.objects.get(product_id=id, variant=variants[0])

            except:
                proDis = 0



        context.update({'sizes': sizes, 'colors': colors, 'variant': variant, 'query': query,
                        'shopcart':shopcart, 'wishlist': wishlist, 'proDis': proDis, })
    else:
        try:
            shopcart = ShopCart.objects.get(user_id=current_user.id, product_id=id)

        except:
            shopcart = 0

        try:
            wishlist = WishList.objects.get(user_id=current_user.id, product_id=id)
        except:
            wishlist = 0

        try:
            proDis = ProductDiscount.objects.get(product_id=id)

        except:
            proDis = 0

        context.update({'shopcart': shopcart, 'wishlist': wishlist, 'proDis': proDis, })

    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)



def search(request):
    current_user = request.user  # Access User Session information
    setting = Setting.objects.get(pk=1)

    wishlist = WishList.objects.filter(user_id=current_user.id)
    myshopcart = ShopCart.objects.filter(user_id=current_user.id)
    variant = Variants.objects.all()

    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                good_matches = Product.objects.filter(Q(title__icontains=query))
                just_ok_matches = Product.objects.filter(Q(title__icontains=query) | Q(keywords__icontains=query)
                                                         | Q(description__icontains=query))

                products = (list(good_matches) + list(just_ok_matches))
                products = pd.Series(products).drop_duplicates().tolist()

                #SearchHistory.objects.filter(user_id=current_user.id).delete()


            else:


                good_matches = Product.objects.filter(Q(title__icontains=query),category_id=catid)
                just_ok_matches = Product.objects.filter(Q(title__icontains=query) | Q(keywords__icontains=query)
                                                         | Q(description__icontains=query),category_id=catid)

                products = (list(good_matches) + list(just_ok_matches))

                products = pd.Series(products).drop_duplicates().tolist()
            print(products)


            SearchHistory.objects.filter(user_id=current_user.id, searchedNow=True).update(searchedNow=False)
            saveFirst = SearchHistory.objects.filter(user_id=current_user.id, searchedNow=False).order_by('-timestamp')[2:]

            for sF in saveFirst:
                sF.delete()

            if(current_user.id):
                for p in products:
                    history = SearchHistory()
                    history.user_id = current_user.id
                    history.product_id = p.id
                    history.searchedNow = True
                    history.searchWord = query
                    history.save()

            category = Category.objects.all()
            context = {'setting' : setting, 'products': products, 'query':query,
                       'wishlist':wishlist, 'myshopcart': myshopcart, 'variant': variant, }
            return render(request, 'search_products.html', context)

        return HttpResponseRedirect('/')

    else:
        history =  SearchHistory.objects.filter(user_id = current_user.id, searchedNow = True)

        products= list()
        for s in history:
            products.append(Product.objects.get(id = s.product_id))

        print(products)
        context = {'setting': setting, 'products': products,
                   'wishlist': wishlist, 'myshopcart': myshopcart, 'variant': variant, }
        return render(request, 'search_products.html', context)


def search_auto(request):
    #setting = Setting.objects.get(pk=1)
    if request.is_ajax():
        q = request.GET.get('term', '')
        good_matches = Product.objects.filter(Q(title__icontains=q)  )
        just_ok_matches = Product.objects.filter(Q(title__icontains=q) | Q(keywords__icontains=q)
                                              | Q(description__icontains=q))

        products = (list(good_matches) + list(just_ok_matches))

        products = pd.Series(products).drop_duplicates().tolist()

        results = []
        for rs in products:
            product_json = {}
            product_json =  rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")

    context = {'faq': faq, 'category': category}
    return render(request, 'faq.html', context)

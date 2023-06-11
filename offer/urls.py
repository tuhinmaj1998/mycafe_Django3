from django.urls import path, include
from . import views

urlpatterns = [
    #/home/main
    path('test/', views.index, name='index'),
    path('plans/', views.plans, name='plans'),
    path('plans/<str:plan>/<str:slug>', views.individualplan, name='individualplan'),
    path('purchaseplan/<int:id>', views.purchaseplan, name='purchaseplan'),
    path('handleRequest/<str:user>', views.handleRequest, name="handleRequest"),
    path('checkvalidcoupon/', views.checkValidCoupon, name="checkValidCoupon"),
]

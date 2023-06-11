from django.urls import path, include
from . import views

urlpatterns = [
    #/home/main
    path('ready', views.make_ready, name='make_ready'),
    path('test', views.test, name='test'),
    path('force-assign-to-delivery', views.forceDelivery, name='forceDelivery'),
    path('', views.index, name='index'),
    path('order-preparing-list/', views.OrderPreparingList, name='OrderPreparingList'),
    path('order-waiting-list/', views.OrderWaitingList, name='OrderWaitingList'),
    path('order-ready-list/', views.OrderReadyList, name='OrderReadyList'),
    path('finish-preparing/<int:id>', views.finishPreparing, name='finishPreparing'),
    path('on-shipping/', views.onShipping, name='onShipping'),

    path('<str:name>/active/scheduled/', views.partnerRunningDelivery, name='partnerRunningDelivery'),
    path('<str:name>/active/current/', views.partnerCurrentDelivery, name='partnerCurrentDelivery'),
    path('<str:name>/active/current/navigation/<int:id>/', views.clickNavigation, name='clickNavigation'),
]



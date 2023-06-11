from django.urls import path, include
from . import views

urlpatterns = [
    #/home/main
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('handleRequest/<str:user>', views.handleRequest, name="handleRequest"),


]
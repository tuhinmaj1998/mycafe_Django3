from django.urls import path, include
from . import views

urlpatterns = [
    #/home/main
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('addreply/<int:id>/<int:cid>', views.addreply, name='addreply'),
    path('', views.index, name='index'),
    path('colors/', views.colors, name='colors'),
    path('addtowishlist/<int:id>/', views.addtowishlist, name='addtowishlist'),



]
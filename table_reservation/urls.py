from django.urls import path, include
from . import views

urlpatterns = [
    #/home/main
    path('', views.table_book, name='make_ready'),
]


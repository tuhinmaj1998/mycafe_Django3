from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from product import views as ProductViews



urlpatterns = [
    #/home/main
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),

    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    path('deletereply/<int:id>/<int:cid>', views.user_deletereply, name='user_deletereply'),

    path('favourites/', ProductViews.wishlist, name='wishlist'),

    path('wallet/', views.user_wallet, name='user_wallet'),
    path('wallet/addmoney/', views.addMoneyToWallet, name='user_wallet'),
    path('wallet/handleRequest/<str:user>', views.walletHandleRequest, name="WalletHandleRequest"),

    path('address/', views.userAddress, name='userAddress'),
    path('address/add-new-address', views.addNewAddress, name='addNewAddress'),

]
# myCafe on Django=3.x.x

Process after cloning.
1. pip install -r requirements.txt
2. try python manage.py runserver
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. Add the user credentials
7. python manage.py runserver
Hopefully now server will up. If not check the errors, probably any package is need to be installed, do it and try again. Happy coding.

It is a prototype of an e-commerce website with django web framework built by Tuhin Majumder. There are several functionalities in this website:

1. Secure login using paytm environment
2. Discount
3. Wallet
4. Cashback and coupon rewards
5. Premium Plans
6. Product varient - size/colour
7. Wishlist
8. Saved Address in user account

All this are from customer perspective. Now there are some functionalities from server end.

1. Delivery partner account
2. Managing Order
3. Delivery Status
4. Optimized algorithm for balancing location+weight to delivery man

Now I am trying to add table reservation app inside this.

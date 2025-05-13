from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.appwelcome),
    path('open_signup/', views.open_signup, name = "open_signup"),
    path('open_signin/', views.open_signin, name = "open_signin"),
    path('sign_up/', views.sign_up, name = "sign_up"),
    path('sign_in/', views.sign_in, name= "sign_in"),
    path('open_add_restaurant/', views.open_add_restaurant, name= "open_add_restaurant"),
    path('add_restaurant/', views.add_restaurant, name="add_restaurant"),
    path('show_restaurant/', views.show_restaurant, name="show_restaurant"),
    path('open_update_restaurant/<str:name>/', views.open_update_restaurant, name="open_update_restaurant"),
    path('update_restaurant/', views.update_restaurant, name="update_restaurant"),
    path('delete_restaurant/<str:name>/', views.delete_restaurant, name="delete_restaurant"),
    path('open_add_menu/<str:name>/', views.open_add_menu, name="open_add_menu"),
    path('add_menu/<str:rname>/', views.add_menu, name="add_menu"),
    path('open_menu/<str:rname>/<str:uname>', views.open_menu, name="open_menu"),
    path('add_to_cart/<str:uname>/<str:rname>/<str:iname>', views.add_to_cart, name = "add_to_cart"),
    path('show_cart_page/<str:username>/', views.show_cart_page, name='show_cart_page'),
    path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/<str:name>/', views.checkout, name="checkout"),
    path('orders/<str:username>/', views.orders, name='orders'),
]
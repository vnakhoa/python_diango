
from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework import routers




urlpatterns = [
    #chuyển hướng vào home
    path('', views.redirect_home, name="redirect_home"),

    path('home', views.homepage, name="home"),
    # path('<int:product_id>', views.homepage, name="home"),

    path('add_cart', views.add_to_cart, name="add_cart"),
    path('cart', views.cart, name="cart"),
    path('incre_descrea', views.incre_descrea, name="incre_descrea"),


    path('<int:product_id>', views.cart_view, name="cart_view"),

    path('checkout', views.checkout, name="checkout"),


    #Form
    path('register', views.register, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),

    # CreateProduct Form
    path('create_product', views.create_product, name='create_product'),

    #Delete product
    path('delete_product', views.delete_product, name='delete_product'),



    path('snippet/', views.SnippetList.as_view()),
    path('snippet/<int:pk>/', views.SnippetDetail.as_view()),

]

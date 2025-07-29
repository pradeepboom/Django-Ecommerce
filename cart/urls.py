from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
 path('',views.cart_summary,name="cart_summary"),
 path('add/', views.add_cart, name='add_cart'),
 path('delete/',views.cart_delete,name="cart_delete"),
 path('update/',views.cart_update,name="cart_update"),
]

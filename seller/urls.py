from django.urls import path
from django.shortcuts import render,redirect 
from . import views
from .views import register,LoginView,seller_logout,add_product,product_list
from django.contrib.auth.decorators import login_required


urlpatterns = [
            path('register',register,name='seller_registration'),
            path('home',login_required(lambda request : render(request,'seller_base.html'),login_url='seller_login'),name='base'),
            path('login',LoginView.as_view(),name='seller_login'),
            path('user/logout',login_required(seller_logout,login_url='seller_login'),name='seller_logout'),
            path('brand/add',views.create_brand,name='add_brand'),
            path('brand/list',views.brand_list,name='brand_list'),
            path('brand/remove/<int:id>',views.delete_brand,name='remove'),
            path('brand/change/<int:id>',views.edit_brand,name='update'),
            path('product/add',login_required(add_product,login_url='seller_login'),name='add_product'),
            path('products',login_required(product_list,login_url='seller_login'),name='listallproducts'),
            path('product/change/<int:id>',views.edit_product,name='edit_product'),
            path('orders',views.OrderListView.as_view(),name='orderlist'),
            path('orders/update/<int:id>',views.OrderChangeView.as_view(),name='update_order'),
            path('orders/count',views.OrderCount.as_view(),name='ordercount')
    
    
]


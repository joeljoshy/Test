from django.urls import path
from .views import RegistrationView,SignInView,HomePageView,ViewProduct,add_to_cart,MyCart,DeleteFromCart,WriteReview,place_order,view_orders,cancel_order
from . import views
urlpatterns=[
    path('register',RegistrationView.as_view(),name='register'),
    path('login',SignInView.as_view(),name='cust_signin'),
    path('signout',views.signout,name='signout'),
    path('home',HomePageView.as_view(),name='customer_home'),
    path('search',views.search,name="search"),
    path('mobiles',views.mobiles,name="mobiles"),
    path('laptops',views.laptops,name="laptops"),
    path('tablets',views.tablets,name="tablets"),
    path('price_low_to_high',views.price_low_to_high,name="price_low_to_high"),
    path('price_high_to_low', views.price_high_to_low, name="price_high_to_low"),

    path("view_profile",views.ViewDetails, name="view_profile"),
    path("edit", views.EditDetails.as_view(), name="edit_profile"),
    path('viewproduct/<int:id>',ViewProduct.as_view(),name='viewproduct'),
    path('addtocart/<int:id>',add_to_cart,name='addtocart'),
    path('mycart',MyCart.as_view(),name='mycart'),
    path('removeitem/<int:pk>',DeleteFromCart.as_view(),name='deletecart'),
    path('review/<int:pk>',WriteReview.as_view(),name='review'),
    path("placeorder/<int:id>/<int:cid>", place_order, name="placeorder"),
    path("vieworders", view_orders, name="vieworders"),
    path("removeorder/<int:id>", cancel_order, name="removeorder"),
    path('viewproduct/<int:id>/writereview',views.WriteReview.as_view(),name='write_review'),
    path('brand/<int:pk>',views.FilterByBrand.as_view(),name='brandfilter'),
    path('base',views.BasePage.as_view(),name='basepage'),
    path('plus/<int:pk>',views.cart_plus,name='plus'),
    path('minus/<int:pk>',views.cart_minus,name='minus'),
    path("checkout", views.CheckoutView, name="checkout"),
    path('summery/<int:id>',views.summery,name='summery'),
    path('deleteaddress/<int:pk>',views.DeleteAddress.as_view(),name='deleteaddress'),
    path('editaddress/int<id>',views.editaddress,name='editaddress'),
    path("order/proceed",views.GatewayView.as_view(),name="index"),
    path("payment", views.charge, name="payment"),



]
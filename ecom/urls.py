"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecomapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("footer",views.footer,name="footer"),    
    path("navbar",views.navbar),
    path("show",views.show),
    path("faq",views.faq1,name="faq"),
    path("contact",views.contact,name="contact"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("myprofile",views.myprofile,name="myprofile"),
    path("changepassword",views.changepassword,name="changepassword"),
    path("editprofile",views.editprofile,name="editprofile"),
    path("categories",views.categories,name="categories"),
    path("showproduct/<str:name>",views.showproduct,name="showproduct"),
    path('showproduct/<str:name>/<str:title>/', views.productdetail, name='productdetail'),
    path("cart/",views.view_cart,name="cart"),
    path("sidebar",views.sidebar,name="sidebar"),
    path("logout",views.logout,name="logout"),
    path("add_to_cart/",views.add_to_cart,name="add_to_cart"),
    path("remove_from_cart/<str:product_title>",views.remove_from_cart,name="remove_from_cart"),
    path("increment_quantity/<str:product_title>",views.increment_quantity,name="increment_quantity"),
    path("decrement_quantity/<str:product_title>",views.decrement_quantity,name="decrement_quantity"),
    path("clear_cart/",views.clear_cart,name="clear_cart"),
    path("forgetpassword/",views.forgetpassword,name="forgetpassword"),
    path("aboutus/",views.aboutus,name="aboutus"),
    path("create_order/", views.create_order, name="create_order"),
    path("save_payment/", views.save_payment, name="save_payment"),
    path("order-history/", views.order_history, name="order_history"),
    path("addresses/", views.manage_addresses, name="manage_addresses"),
    path("select-shipping/", views.select_shipping, name="select_shipping"),
    path("", views.homepage, name="homepage"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("chat/", views.chat, name="chat"),
    path('cod-order/', views.cod_order, name="cod_order"),


    







]

urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

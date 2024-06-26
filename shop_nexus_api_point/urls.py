"""
URL configuration for shop_nexus_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include
from rest_framework import routers
from .views import * 
from .models import *

router = routers.DefaultRouter()
router.register(r'products', ProductViewset, basename=Product)
router.register(r'orderitems', OrderItemViewset, basename=OrderItem)
router.register(r'seller-product', SellerProductViewset, basename=Product)
router.register(r'seller', SellerViewset, basename=Seller)


urlpatterns = [
    path('', include(router.urls)),
    path('customer-register/', CustomerRegisterView.as_view()),
    path('customer-login/', LoginView.as_view()),
    path('seller-login/', SellerLoginView.as_view()),
    path('seller-register/', SellerRegView.as_view()),
    path('get-user-details/', GetSecuredData.as_view()),
    path('make_payment/', PaymentViewset.as_view()),
    path('last_payment/', LastPaymentViewset.as_view()),
    path('orders/', InvoiceViewset.as_view()),
    path('seller-orders/', SellerOrder.as_view()),
    path('seller-product-fetch/', SellerProductFetch.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
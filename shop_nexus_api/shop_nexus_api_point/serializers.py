from rest_framework import serializers
from .models import *

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class ProductSerializers(serializers.ModelSerializer):
    seller = SellerSerializer()
    class Meta:
        model = Product
        fields = '__all__'

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializers()
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'customer', 'quantity')
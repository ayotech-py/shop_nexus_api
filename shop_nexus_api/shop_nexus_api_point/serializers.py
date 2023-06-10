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
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
import jwt
from .models import Jwt
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import json

def get_rand(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# the function generates access token: an access token hold the information of a logged in user


def get_access_token(payload):
    return jwt.encode(
        {
            "exp": datetime.now() + timedelta(minutes=30), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

# this function  generates a refresh token for the access tokent to renewed


def get_refresh_token():
    return jwt.encode(
        {
            "exp": datetime.now() + timedelta(days=365), "data": get_rand(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

class OrderItemViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        product = request.data['product']
        customer = request.data['customer']
        user = User.objects.get(username=customer)
        customer = Customer.objects.get(user=user)

        product = Product.objects.get(id=product)
        order_item = OrderItem.objects.create(customer=customer, product=product, quantity=1)
        serializer = self.get_serializer(order_item)
        return Response(serializer.data, status=200)
    
    def destroy(self, request, *args, **kwargs):
        product = request.data['product']
        customer = request.data['customer']
        user = User.objects.get(username=customer)
        customer = Customer.objects.get(user=user)

        product = Product.objects.get(id=product)
        OrderItem.objects.filter(product=product).delete()
        return Response({'success':'item deleted'}, status=200)

class CustomerRegisterView(APIView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        data = request.data

        user = authenticate(email=data['email'])

        if user:
            return Response({"error": "Username or Email already exist"}, status=400)

        try:
            user = User.objects.create_user(username=data['email'], password=data['password'])
            print(type(data['phone']))
            user.save()
            Customer.objects.create(user_id=user.id, name=data['name'], phone=int(data['phone']), address=data['address'])
            return Response({"success": "Your account has been successfully created"})
        except Exception as e:
            print(e)
            return Response({"error": "Username or Email already exist"}, status=400)
    
    
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "invalid login or password"}, status=400)

        Jwt.objects.filter(user_id=user.pk).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(user_id=user.id, access=access, refresh=refresh)

        return Response({"access": access, "refresh": refresh, "username": user.username})

# the class renews the access token with the refresh token
class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data['refresh'])
        except Exception:
            return Response({"error": "Refresh token doesnt exist"}, status=400)

        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response({"error": "Token is invalid of has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access
        active_jwt.refresh = refresh

        active_jwt.save()

        return Response({"access": access, "refresh": refresh})

class GetSecuredData(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        user = Customer.objects.get(user=user_id)
        orders = OrderItem.objects.filter(customer=user.id)
        serialized_order = OrderItemSerializer(orders, many=True)
        print(serialized_order.data)
        context = {
            'name': user.name,
            'address': user.address,
            'phone': user.phone,
            'orderitems': serialized_order.data,
        }
        return Response({'data': context})
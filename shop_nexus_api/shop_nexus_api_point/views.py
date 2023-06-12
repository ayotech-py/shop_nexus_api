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


class CustomerRegisterView(APIView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['user'],)

        if user:
            return Response({"error": "Username or Email already exist"}, status=400)

        try:
            user = User.objects.create_user(username=serializer.validated_data['email'], password=serializer.validated_data['password'])
            user.save()
            user_id = user.username
            Customer.objects.create(user=user_id, **serializer.validated_data)
            return Response({"success": "Your account has been successfully created"})
        except Exception:
            return Response({"error": "Username or Email already exist"}, status=400)
    
    def get(self, request):
        customer = Customer.objects.filter(id>=0)
        return Response({'data': json.dumps(customer)})


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

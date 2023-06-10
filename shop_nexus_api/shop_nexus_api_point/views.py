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

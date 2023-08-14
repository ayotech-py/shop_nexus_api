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
from django.core.files.base import ContentFile
import base64
from django.conf import settings
import requests


def get_rand(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# the function generates access token: an access token hold the information of a logged in user


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=30), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


# this function  generates a refresh token for the access tokent to renewed


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_rand(10)},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def convertImage(image):
    name = "photo"
    format, imgstr = image.split(";base64,")
    ext = format.split("/")[-1]
    image_file = ContentFile(base64.b64decode(imgstr), name=f"{name}.{ext}")
    return image_file


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.headers["user"]
        user_id = User.objects.get(username=user)
        seller_id = Seller.objects.get(user_id=user_id.id)
        data = request.data
        images = data["images"]

        newProduct = Product.objects.create(
            seller_id=seller_id.id,
            image=convertImage(images[0]),
            img_1=convertImage(images[1]),
            img_2=convertImage(images[2]),
            img_3=convertImage(images[3]),
            img_4=convertImage(images[4]),
            name=data["name"],
            description=data["description"],
            price=data["price"],
            category=data["category"],
            count=data["quantity"],
            rating=4,
            featured=False,
        )

        serializer = self.get_serializer(newProduct)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        user = request.headers["user"]
        user_id = User.objects.get(username=user)
        seller_id = Seller.objects.get(user_id=user_id.id)
        data = request.data
        return Response(status=200)


class OrderItemViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        product = request.data["product"]
        customer = request.data["customer"]
        user = User.objects.get(username=customer)
        customer = Customer.objects.get(user=user)

        product = Product.objects.get(id=product)
        order_item = OrderItem.objects.create(
            customer=customer, product=product, quantity=1
        )
        serializer = self.get_serializer(order_item)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        product = request.data["product"]
        customer = request.data["customer"]
        quantity = request.data["quantity"]
        user = User.objects.get(username=customer)
        customer = Customer.objects.get(user=user)

        product = Product.objects.get(id=product)
        orderitem = OrderItem.objects.get(customer=customer.id, product=product)
        orderitem.quantity = quantity
        orderitem.save()
        print(orderitem.quantity)
        return Response({"success": "item increased"}, status=200)

    def destroy(self, request, *args, **kwargs):
        product = request.data["product"]
        customer = request.data["customer"]
        user = User.objects.get(username=customer)
        customer = Customer.objects.get(user=user)

        product = Product.objects.get(id=product)
        OrderItem.objects.filter(product=product).delete()

        return Response({"success": "item deleted"}, status=200)


class CustomerRegisterView(APIView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        data = request.data

        user = authenticate(email=data["email"])

        if user:
            return Response({"error": "Username or Email already exist"}, status=400)

        try:
            user = User.objects.create_user(
                username=data["email"], password=data["password"]
            )
            user.save()
            Customer.objects.create(
                user_id=user.id,
                name=data["name"],
                phone=int(data["phone"]),
                address=data["address"],
            )
            return Response({"success": "Your account has been successfully created"})
        except Exception as e:
            print(e)
            return Response({"error": "Username or Email already exist"}, status=400)


class SellerRegView(APIView):
    def post(self, request):
        data = request.data
        name = "photo"
        image = data["image"]
        format, imgstr = image.split(";base64,")
        ext = format.split("/")[-1]
        image_file = ContentFile(base64.b64decode(imgstr), name=f"{name}.{ext}")

        if User.objects.filter(username=data["email"]).exists():
            return Response({"error": "Username or Email already exist"}, status=400)

        try:
            user = User.objects.create_user(
                username=data["email"], password=data["password"]
            )
            Seller.objects.create(
                user_id=user.id,
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                address=data["address"],
                bio=data["bio"],
                about=data["about"],
                rating=5,
                business_name=data["businessname"],
                business_category=data["businesscategory"],
                business_reg_no=data["businessreg"],
                business_logo=image_file,
            )
            user.save()
            return Response({"success": "Your account has been successfully created"})
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=400)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response({"error": "invalid email or password"}, status=400)

        check_user = Customer.objects.filter(user_id=user.id).exists()

        if not check_user:
            return Response({"error": "invalid emall or password"}, status=400)

        Jwt.objects.filter(user_id=user.pk).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(user_id=user.id, access=access, refresh=refresh)

        return Response(
            {"access": access, "refresh": refresh, "username": user.username}
        )


class SellerLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response({"error": "invalid login or password"}, status=400)

        check_user = Seller.objects.filter(user_id=user.id).exists()
        if not check_user:
            return Response({"error": "invalid login or password"}, status=400)

        Jwt.objects.filter(user_id=user.pk).delete()

        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(user_id=user.id, access=access, refresh=refresh)

        return Response(
            {"access": access, "refresh": refresh, "username": user.username}
        )


# the class renews the access token with the refresh token
class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Exception:
            return Response({"error": "Refresh token doesnt exist"}, status=400)

        if not Authentication.verify_token(serializer.validated_data["refresh"]):
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
        orders = OrderItem.objects.filter(customer=user.id, status=False)
        serialized_order = OrderItemSerializer(orders, many=True)
        for i in range(len(serialized_order.data)):
            image = serialized_order.data[i]["product"]["image"]
            img_1 = serialized_order.data[i]["product"]["img_1"]
            img_2 = serialized_order.data[i]["product"]["img_2"]
            img_3 = serialized_order.data[i]["product"]["img_3"]
            img_4 = serialized_order.data[i]["product"]["img_4"]

            serialized_order.data[i]["product"]["image"] = (
                "http://127.0.0.1:8000" + image
            )
            serialized_order.data[i]["product"]["img_1"] = (
                "http://127.0.0.1:8000" + img_1
            )
            serialized_order.data[i]["product"]["img_2"] = (
                "http://127.0.0.1:8000" + img_2
            )
            serialized_order.data[i]["product"]["img_3"] = (
                "http://127.0.0.1:8000" + img_3
            )
            serialized_order.data[i]["product"]["img_4"] = (
                "http://127.0.0.1:8000" + img_4
            )

        context = {
            "name": user.name,
            "address": user.address,
            "phone": user.phone,
            "orderitems": serialized_order.data,
        }
        return Response({"data": context})


class SellerViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SellerSerializer

    def get_queryset(self):
        data = self.request.headers
        user = data["User"]
        user_id = User.objects.get(username=user)
        print(user_id.id)
        return Seller.objects.filter(user_id=user_id.id)


class SellerProductViewset(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializers

    def get_queryset(self):
        data = self.request.headers
        user = data["User"]
        user_id = User.objects.get(username=user)
        print(user_id.id)
        try:
            seller_id = Seller.objects.get(user_id=user_id.id)
            return Product.objects.filter(seller_id=seller_id.id)
        except Exception:
            return Response({"error": "Seller does not exist"}, status=400)


class LastPaymentViewset(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user
        customer = Customer.objects.get(user_id=user_id.id)
        queryset = Payment.objects.filter(customer_id=customer.id)
        last_order = list(queryset)[-1]
        return Response({"data": last_order.transaction_id})


class InvoiceViewset(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user
        customer = Customer.objects.get(user_id=user_id.id)
        queryset = Order.objects.filter(customer=customer.id)
        queryset = list(queryset)[-1]
        order_list = eval(queryset.orderitem_list)
        orders = OrderItem.objects.filter(id__in=order_list)
        serialized_order = OrderItemSerializer(orders, many=True)

        context = {"orders": serialized_order.data, "status": 200}
        return Response(context)


class SellerOrder(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.request.headers
        user = data["User"]
        user_id = User.objects.get(username=user)
        try:
            seller_id = Seller.objects.get(user_id=user_id.id)
            fetched_order = OrderItem.objects.filter(
                product__seller__id=seller_id.id, status=True
            )
            serializer = OrderItemSerializer(fetched_order, many=True)
            return Response(serializer.data, status=200)
        except Exception:
            return Response({"error": "Seller does not exist"}, status=400)


class PaymentViewset(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializers_class = PaymentSerializer

    def get(self, request):
        user_id = request.user
        email = user_id.username
        customer = Customer.objects.get(user_id=user_id.id)
        ref_id = request.GET["ref_id"]
        url = "https://api.paystack.co/transaction/verify/{}".format(ref_id)
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers)
        response = r.json()

        if response["status"]:
            status = response["data"]["status"]
            payment = Payment.objects.get(transaction_id=ref_id)
            order_list = eval(payment.order.orderitem_list)
            for i in order_list:
                queryset = OrderItem.objects.get(id=i)
                queryset.status = True
                queryset.save()
            payment.status = status
            payment.save()
            name = payment.customer.name
            order = payment.order.id
            time = payment.timestamp
            amount = payment.amount
            status = payment.status
            transaction_id = payment.transaction_id

            context = {
                "name": name,
                "order_id": order,
                "time": time,
                "amount": amount,
                "status": status,
                "transaction_id": transaction_id,
            }

            return Response(context, status=200)
        else:
            return Response(response, status=400)

    def post(self, request):
        data = self, request.data
        user_id = request.user
        email = user_id.username
        customer = Customer.objects.get(user_id=user_id.id)
        orderitem = OrderItem.objects.filter(customer_id=customer.id, status=False)
        amount = 0
        order_id = []
        for item in list(orderitem):
            order_id.append(item.id)
            quantity = item.quantity
            price = item.product.price
            sum = quantity * price
            amount = amount + sum
        body = {
            "amount": (amount + 1000) * 100,
            "email": email,
            "callback_url": "https://shop-nexus-xi.vercel.app/payment-receipt/invoice",
        }
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.post(url, headers=headers, data=body)
        response = r.json()
        order_created = Order.objects.create(
            customer=customer, orderitem_list=str(order_id), total_amount=amount + 1000
        )
        order_created.save()
        Payment.objects.create(
            customer=customer,
            amount=amount,
            order_id=order_created.id,
            status="pending",
            transaction_id=response["data"]["reference"],
        )
        return Response(
            {"redirect_url": response["data"]["authorization_url"]}, status=200
        )

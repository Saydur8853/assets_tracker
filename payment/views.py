from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response

from sslcommerz_client.client import SSLCommerzClient
from .serializers import (
    PaymentInitSerializer,
    PaymentStreamSerializer,
    TransactionSerializer,
)
from .models import (
    SSLCommerzPaymentSettings as settings,
    PaymentStream,
    Order,
    Transaction,
)
from .utils import tran_id_generator

from rest_framework import mixins, viewsets


class PaymentStreamViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PaymentStream.objects.filter(is_active=True)
    serializer_class = PaymentStreamSerializer


class PaymentInitAPIView(APIView):
    def post(self, request):
        credentials = settings.for_site(site).get_credentials()
        store_id = credentials["store_id"]
        store_passwd = credentials["store_pass"]
        sandbox = credentials["is_sandbox"]

        client = SSLCommerzClient(
            store_id=store_id,
            store_passwd=store_passwd,
            sandbox=sandbox,
        )
        serializer = PaymentInitSerializer(data=request.data, many=False)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            donation_steam = serializer.validated_data["donation_stream"]
            name = serializer.validated_data["name"]
            email = serializer.validated_data["email"]
            reminder = serializer.validated_data["reminder"]

            url = request.build_absolute_uri(reverse("payment-status"))

            steam = PaymentStream.objects.get(id=int(donation_steam))

            tran_id = tran_id_generator()
            tran_obj = Transaction.objects.create(tran_id=tran_id, amount=amount)

            order_obj = Order.objects.create(
                transaction=tran_obj,
                amount=amount,
                donation_steam=steam,
                name=name,
                email=email,
                reminder=reminder,
            )

            post_data = {
                "total_amount": amount,
                "currency": "BDT",
                "tran_id": tran_id,
                "product_category": "donation",
                "success_url": url,
                "fail_url": url,
                "cancel_url": url,
                "cus_name": name,
                "cus_email": email,
                "shipping_method": "NO",
                "num_of_item": 1,
                "product_name": "donation",
                "product_category": "donation",
                "product_profile": "general",
                "cus_add1": "Some Address",
                "cus_city": "Dhaka",
                "cus_country": "Bangladesh",
                "cus_phone": "01XX-XXXXXXX",
            }

            res = client.initiateSession(post_data)
            return Response(data=res.response.dict())


@csrf_exempt
def payment_response(request):
    if request.method == "POST":
        payment_data = request.POST
        tran_id = payment_data["tran_id"]
        url = f"https:urlhere{tran_id}"
        tran_obj = Transaction.objects.get(tran_id=tran_id)
        order_obj = Order.objects.get(transaction=tran_obj)
        if payment_data["status"] == "VALID":
            tran_obj.tran_status = "success"
            tran_obj.store_amount = payment_data["store_amount"]
            tran_obj.api_response = payment_data
            tran_obj.save()
            order_obj.status = "paid"
            order_obj.save()
            return redirect(url)
        elif payment_data["status"] == "FAILED":
            tran_obj.tran_status = "failed"
            tran_obj.api_response = payment_data
            tran_obj.save()
            return redirect(url)
        elif payment_data["status"] == "CANCELLED":
            tran_obj.tran_status = "cancel"
            tran_obj.api_response = payment_data
            tran_obj.save()
            return redirect(url)


class TransactionViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "tran_id"

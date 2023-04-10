from rest_framework import serializers
from .models import (
    PaymentStream,
    Order,
    Transaction,
    SSLCommerzPaymentSettings as settings,
)


class PaymentInitSerializer(serializers.Serializer):
    amount = serializers.CharField()
    donation_stream = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    reminder = serializers.BooleanField()


class PaymentStreamSerializer(serializers.ModelSerializer):
    project_url = serializers.SerializerMethodField()
    raised_amount = serializers.SerializerMethodField()

    class Meta:
        model = PaymentStream
        fields = "__all__"

    def get_project_url(self, obj):
        if obj.project:
            return obj.project.get_url()
        return ""

    def get_raised_amount(self, obj):
        all_donations = Order.objects.filter(donation_steam=obj.id, status="paid")
        if all_donations:
            amounts = []
            for donation_data in all_donations:
                amount = donation_data.transaction.store_amount
                amounts.append(amount)
            return sum(amounts)
        return 0


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    redirect_url = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        # fields = "__all__"
        exclude = ["api_response", "created_at", "updated_at"]

    def get_order(self, obj):
        order = Order.objects.get(transaction=obj)
        return OrderSerializer(order, many=False).data

    def get_redirect_url(self, obj):
        pass
        # return urls["redirect_url"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

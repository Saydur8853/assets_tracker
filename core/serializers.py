from rest_framework import serializers
from .models import Company, Device


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    checked_out_by = serializers.StringRelatedField()

    class Meta:
        model = Device
        fields = "__all__"

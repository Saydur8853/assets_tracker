from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Company, Device
from .serializers import CompanySerializer, DeviceSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

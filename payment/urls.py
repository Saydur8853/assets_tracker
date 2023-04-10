from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentStreamViewSet

router = DefaultRouter()
router.register(r"donation-streams", PaymentStreamViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet, BrandViewSet

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'brands', BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

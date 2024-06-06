from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('brands/<int:manufacturer_id>/', views.brands, name='brands'),
]

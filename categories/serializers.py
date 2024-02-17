from rest_framework import serializers
from products.serializers import ProductListSerializer
from products.models import Product
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)
    class Meta:
        model = Category
        fields = ['name','is_active','count_products','products']
from rest_framework import serializers

from products.models import Product,Sku


class ProductListSerializer(serializers.ModelSerializer):
    """
    To show list of products.
    """

    class Meta:
        model = Product
        fields = ["name","description","ingredients"]

class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = ['product','measurement_unit','size','status','selling_price','platform_commission','cost_price']
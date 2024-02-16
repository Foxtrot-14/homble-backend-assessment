from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)

from .models import Product
from .serializers import ProductListSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def products_list(request):
    """
    List of all products.
    """
    if request.GET:
        param_value = request.GET.get('type')
        if param_value=='refrigerated':
            products = Product.objects.filter(is_refrigerated=1)
            serializer = ProductListSerializer(products, many=True)
            return Response({"products": serializer.data}, status=HTTP_200_OK)
        if param_value=='not-refrigerated':
            products = Product.objects.filter(is_refrigerated=0)
            serializer = ProductListSerializer(products, many=True)
            return Response({"products": serializer.data}, status=HTTP_200_OK)
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response({"products": serializer.data}, status=HTTP_200_OK)

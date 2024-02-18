from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.permissions import BasePermission
from .models import Product, Sku
from .serializers import ProductListSerializer,SkuSerializer

sku_queryset = Sku.objects.all()

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        # Check if the user exists and belongs to the "Supervisors" group
        return request.user and request.user.groups.filter(name='Supervisors').exists()
    
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

@api_view(["GET"])
@permission_classes([AllowAny])
def product_details(request,pk):
    try:
        product = Product.objects.get(pk = pk)
        Pserializer = ProductListSerializer(product)
        sku = Sku.objects.filter(product=pk,status=2)
        Sserializer = SkuSerializer(sku, many=True)
        for item in Sserializer.data:
            platform_commission = item['platform_commission']
            cost_price = item['cost_price']
            markup_percentage = (platform_commission / cost_price) * 100
            item['markup_percentage'] = markup_percentage
        return Response([{"product":Pserializer.data,"Skus":Sserializer.data}],status=HTTP_200_OK)
    except Product.DoesNotExist or Sku.DoesNotExist:
        return Response({'msg':"Product not found"}, status=HTTP_404_NOT_FOUND)  
        
@api_view(["POST"])
@permission_classes([IsStaff])
def sku_list(request):
    serializer = SkuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "sku created"}, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsSupervisor, IsStaff])
def sku_list_edit(request,pk):
    sku = sku_queryset.filter(id=pk).first()
    serializer = SkuSerializer(sku, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "sku edited"}, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.serializers import serialize
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.permissions import BasePermission
from .models import Product, Sku
from categories.models import Category
from .serializers import ProductListSerializer,SkuSerializer
from django.db.models import Count, Q
from django.http import JsonResponse

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

@api_view(["GET"])
@permission_classes([AllowAny])
def category_sku(request):    
    active_categories_with_sku_count = Category.objects.filter(
        is_active=True
    ).annotate(
        num_approved_skus=Count('products__sku', filter=Q(products__sku__status=2))
    ).values('name', 'num_approved_skus')
    categories_list = list(active_categories_with_sku_count)
    return JsonResponse(categories_list, safe=False)
    '''
    Response obtained from the above view
    the request has been updated in the postman_collection file
    [
        {
            "name": "Cereals",
            "num_approved_skus": 0
        },
        {
            "name": "Baked Goods",
            "num_approved_skus": 2
        }
    ]
    '''
@api_view(["GET"])
@permission_classes([AllowAny])
def skus_category(request):
    data = Sku.objects.select_related('product__category')
    json_data = serialize('json', data, fields = ('product','measurement_unit','size','status','selling_price','platform_commission','cost_price','product__category'))
    return JsonResponse(json_data, safe=False)   
    '''
    Response obtained from the above view
    the request has been updated in the postman_collection file
        "[{\"model\": \"products.sku\", \"pk\": 5, \"fields\": {\"product\": 6, \"measurement_unit\": \"gm\", \"size\": 250, \"status\": 1, \"selling_price\": 50, \"platform_commission\": 12.5, \"cost_price\": 37.5}}, {\"model\": \"products.sku\", \"pk\": 6, \"fields\": {\"product\": 6, \"measurement_unit\": \"gm\", \"size\": 500, \"status\": 2, \"selling_price\": 69, \"platform_commission\": 17, \"cost_price\": 52}}, {\"model\": \"products.sku\", \"pk\": 7, \"fields\": {\"product\": 4, \"measurement_unit\": \"gm\", \"size\": 100, \"status\": 2, \"selling_price\": 14, \"platform_commission\": 3, \"cost_price\": 11}}, {\"model\": \"products.sku\", \"pk\": 8, \"fields\": {\"product\": 4, \"measurement_unit\": \"gm\", \"size\": 1000, \"status\": 1, \"selling_price\": 100, \"platform_commission\": 25, \"cost_price\": 75}}, {\"model\": \"products.sku\", \"pk\": 9, \"fields\": {\"product\": 4, \"measurement_unit\": \"gm\", \"size\": 300, \"status\": 2, \"selling_price\": 60, \"platform_commission\": 15, \"cost_price\": 45}}, {\"model\": \"products.sku\", \"pk\": 10, \"fields\": {\"product\": 8, \"measurement_unit\": \"gm\", \"size\": 50, \"status\": 1, \"selling_price\": 10, \"platform_commission\": 2.5, \"cost_price\": 7.5}}, {\"model\": \"products.sku\", \"pk\": 11, \"fields\": {\"product\": 8, \"measurement_unit\": \"gm\", \"size\": 100, \"status\": 2, \"selling_price\": 14, \"platform_commission\": 3, \"cost_price\": 11}}, {\"model\": \"products.sku\", \"pk\": 12, \"fields\": {\"product\": 3, \"measurement_unit\": \"gm\", \"size\": 500, \"status\": 2, \"selling_price\": 102, \"platform_commission\": 2, \"cost_price\": 100}}]"
    '''
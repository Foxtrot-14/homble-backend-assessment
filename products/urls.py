from django.urls import path

from .views import products_list,sku_list,product_details,sku_list_edit

urlpatterns = [
    path("", products_list, name="products-list"),
    path("<int:pk>", product_details, name="product-details"),
    path("sku", sku_list, name="sku-list"),
    path("sku-edit/<int:pk>",sku_list_edit,name="sku-edit"),
]

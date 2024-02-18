from django.urls import path

from .views import products_list,sku_list,product_details,sku_list_edit,category_sku,skus_category

urlpatterns = [
    path("", products_list, name="products-list"),
    path("<int:pk>", product_details, name="product-details"),
    path("sku", sku_list, name="sku-list"),
    path("sku-edit/<int:pk>",sku_list_edit,name="sku-edit"),
    path("category-sku",category_sku,name="category-sku"),
    path("sku-category",skus_category,name="sku-category"),
]

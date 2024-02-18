from django.contrib import admin

from products.models import Product,Sku


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "managed_by")
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category")
    fields = (
        ("name"),
        ("category", "is_refrigerated"),
        "description",
        "ingredients",
        ("id", "created_at","edited_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at","edited_at")

@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_display = ("product","size", "selling_price","platform_commission","cost_price")
    ordering = ("-id",)
    search_fields = ("product",)
    list_filter = ("size", "selling_price")
    fields = (
        ("id","product","size","measurement_unit","status", "selling_price","platform_commission","cost_price"),
    )
    autocomplete_fields = ("product",)
    readonly_fields = ("id",)

class SkuInline(admin.StackedInline):
    model = Sku
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("id",)
    fields = (readonly_fields,)
    show_change_link = True
    
class ProductInline(admin.StackedInline):
    """
    For display in CategoryAdmin
    """

    model = Product
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("name","is_refrigerated")
    fields = (readonly_fields,)
    show_change_link = True
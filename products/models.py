from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

STATUS_TYPE = (
    (1,"Pending for Approval (default)"),
    (2,"Approved"),
    (3,"Discontinued"),
)

def validate_size(value):
    if value > 999:
        raise ValidationError('Size cannot exceed 999.')

class SkuQuerySet(models.QuerySet):
    def create(self, *args, **kwargs):
        kwargs['status'] = 1  # Set status to 1 regardless of the value provided
        return super().create(*args, **kwargs)

class Product(models.Model):
    """
    Very basic structure. To be further built up.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )
    description = models.TextField(
        _("descriptive write-up"),
        unique=True,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    ingredients = models.CharField(
        _("Ingredients"),
        max_length=500,
        help_text=_("List of ingredients (up to 500 characters)"),
        default="empty",
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        # Just to be explicit.
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Sku(models.Model):
    MEASUREMENT_UNITS = [
        ('gm', 'Grams'),
        ('kg', 'Kilograms'),
        ('mL', 'Milliliters'),
        ('L', 'Liters'),
        ('pc', 'Piece'),
    ]
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        "Product",
        related_name="sku",
        null=False,
        on_delete=models.PROTECT,
    )
    measurement_unit = models.CharField(max_length=2, choices=MEASUREMENT_UNITS,default='gm')
    size = models.PositiveSmallIntegerField(
        _("size in grams"),
        help_text=_("Size visible to the customer (gm.)"),
        validators=[validate_size]
    )
    status = models.IntegerField(choices=STATUS_TYPE, default=1)
    selling_price = models.PositiveSmallIntegerField(
        _("selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
    )
    platform_commission = models.PositiveSmallIntegerField(
        _("platform commission"),
        help_text=_("Platform Commission"),
        blank=True,
    )
    cost_price = models.PositiveSmallIntegerField(
        _("cost price"),
        help_text=_("Cost Price"),
        blank=True,
    )
    objects = SkuQuerySet.as_manager()    
    def save(self, *args, **kwargs):
        self.selling_price = self.cost_price+self.platform_commission
        super().save(*args,**kwargs)
        
    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        # Just to be explicit.
        db_table = "sku"
        ordering = []
        verbose_name = "Sku"
        verbose_name_plural = "Skus"
        unique_together = ['product', 'selling_price']
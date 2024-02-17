from django.core.management.base import BaseCommand
from products.models import Sku
from django.db.models import F

class Command(BaseCommand):
    help = 'Update platform_commission and cost_price based on selling_price'

    def handle(self, *args, **options):
        Sku.objects.update(platform_commission=F('selling_price') * 0.25)
        Sku.objects.update(cost_price=F('selling_price') - F('platform_commission'))

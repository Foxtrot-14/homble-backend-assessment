# Generated by Django 3.2.24 on 2024-02-17 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_sku_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='size',
            field=models.PositiveSmallIntegerField(help_text='Size visible to the customer (gm.)', verbose_name='size in grams'),
        ),
    ]

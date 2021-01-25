# Generated by Django 3.1.5 on 2021-01-25 08:13

from django.db import migrations


def add_available_fields(apps, schema_editor):
    """Add available value in exists objects"""
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Product = apps.get_model('main', 'Product')
    for product in Product.objects.all():
        product.available = True
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_available'),
    ]

    operations = [
        migrations.RunPython(add_available_fields)
    ]

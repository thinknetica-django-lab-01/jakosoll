from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from main.models import Product
from main.models import Category
from main.models import Vendor


class ProductModelTest(TestCase):

    def test_cannot_save_empty_product_name(self):
        """Test: cannot save product without name"""
        category = Category.objects.create()
        product = Product(price=10, category=category)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_product_related_with_category(self):
        """Test: product related with category"""
        category = Category.objects.create()
        product = Product(price=10)
        product.category = category
        product.save()
        self.assertIn(product, category.product_set.all())

    def test_string_representation(self):
        """Test: product str representation"""
        product = Product(name='Some name')
        self.assertEqual(str(product), 'Some name')


class VendorModelsTest(TestCase):

    def test_vendors_post_save(self):
        """Test: vendor create when created User"""
        user = User.objects.create_user(username='name')
        vendor = Vendor.objects.first()
        self.assertEqual(user.vendor.id, vendor.id)

    def test_string_representation(self):
        """Test: product str representation"""
        User.objects.create_user(username='name')
        vendor = Vendor.objects.first()
        self.assertEqual(str(vendor), 'name')

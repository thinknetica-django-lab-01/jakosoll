from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Product
from main.models import Category
from main.models import Tag
from main.models import Vendor


class VendorModelsTest(TestCase):

    def test_vendors_post_save(self):
        user = User.objects.create_user(username='name')
        vendor = Vendor.objects.first()
        self.assertIsInstance(user.vendor, vendor)
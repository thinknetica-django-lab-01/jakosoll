from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from main.models import Product
from main.models import Category
from main.models import Profile


class ProductModelTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='name')
        self.category = category = Category.objects.create(name='test_category')

    def test_cannot_save_empty_product_name(self):
        """Test: cannot save product without name"""
        product = Product(price=10, category=self.category, vendor=self.user)
        with self.assertRaises(ValidationError):
            product.save()
            product.full_clean()

    def test_product_related_with_category(self):
        """Test: product related with category"""
        product = Product(name='test_item', price=10, vendor=self.user)
        product.category = self.category
        product.save()
        self.assertIn(product, self.category.product_set.all())

    def test_string_representation(self):
        """Test: product str representation"""
        product = Product.objects.create(
            name='Some name',
            category=self.category,
            price=10,
            vendor=self.user
        )
        self.assertEqual(str(product), 'Some name')


class ProfileModelsTest(TestCase):


    def test_Profiles_post_save(self):
        """Test: Profile create when created User"""
        user = User.objects.create_user(username='name')
        profile = Profile.objects.first()
        self.assertEqual(user.profile.id, profile.id)

    def test_Profile_string_representation(self):
        """Test: Profile str representation"""
        User.objects.create_user(username='name')
        profile = Profile.objects.first()
        self.assertEqual(str(profile), 'name')

    def test_User_in_sellers_when_Profile_make_as_vendor(self):
        """
        Test: User was added in sellers group when make as vendor
        """
        user = User.objects.create_user(username='name')

        self.assertFalse(
            user.groups.filter(name='sellers').exists(), 
            msg="Error, user in sellers group"
        )

        user.profile.make_as_vendor()
        self.assertTrue(
            user.groups.filter(name='sellers').exists(), 
            msg="User out of sellers group"
        )






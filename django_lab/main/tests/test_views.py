from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve
from main.views import index, ProductListView
from main.models import Product, Category


class MainViewsTest(TestCase):
    """testcases for views"""
    
    def test_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_main_page_uses_right_template(self):
        """test: main page uses index.html"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_status_code(self):
        """test: view returns 200 status"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ListViewSTest(TestCase):

    def test_url_resolve_has_right_name(self):
        """Test: apps has right name"""
        found = resolve('/goods/')
        self.assertEqual(found.view_name, 'goods')

    def test_list_page_uses_right_template(self):
        """Test; list view uses product_list.html"""
        response = self.client.get('/goods/')
        self.assertTemplateUsed(response, 'product_list.html')

    def test_page_shows_list_of_products(self):
        """Test: goods displays on list page"""
        user = User.objects.create_user(username='test', password='123456')
        category1 = Category.objects.create(name='Category 1', slug='category-1')
        Product.objects.create(name='product 1', price=100, category=category1, vendor=user)
        Product.objects.create(name='product 2', price=200, category=category1, vendor=user)
        response = self.client.get('/goods/')
        self.assertContains(response, 'product 1')
        self.assertContains(response, 'product 2')
        self.assertNotContains(response, 'product 3')

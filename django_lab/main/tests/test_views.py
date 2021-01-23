from django.test import TestCase
from django.urls import resolve
from main.views import index


class MainViewsTest(TestCase):
    """testcases for views"""
    def test_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_main_page_uses_right_template(self):
        """test: main page uses index.html"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

import pytest
from main.models import Category, Product


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def user(django_user_model):
    return django_user_model.objects.create(
        username='test', password='123456'
    )


@pytest.fixture()
def product(django_user_model, user):
    category1 = Category.objects.create(name='Category 1', slug='category-1')
    product = Product.objects.create(
        name='product 1', price=100, category=category1, vendor=user
    )
    return product

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
def product(django_user_model, user, category):
    product = Product.objects.create(
        name='product 1', price=100, category=category, vendor=user
    )
    return product


@pytest.fixture()
def vendor_client(user, client):
    user.profile.make_as_vendor()
    client.force_login(user)
    return client


@pytest.fixture()
def category():
    return Category.objects.create(name='Category 1', slug='category-1')

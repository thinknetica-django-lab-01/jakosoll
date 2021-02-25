from main.management.commands.dummyitems import (
    get_or_create_categories,
    get_or_create_tags,
    get_or_create_vendors
)
from main.models import Category, Tag


def test_get_or_create_categories_returns_right_amount():
    """Test: func returns right categories amount"""
    Category.objects.create(name='test', slug='test123')
    categories = get_or_create_categories(10)
    assert len(categories) == 9


def test_get_or_create_categories_returns_list():
    """Test: func returns list object"""
    categories = get_or_create_categories(10)
    assert isinstance(categories, list)


def test_get_or_create_tags_returns_right_amount():
    """Test: func returns right tags amount"""
    Tag.objects.create(name='test_tag')
    tags = get_or_create_tags(10)
    assert len(tags) == 9


def test_get_or_create_tags_returns_list():
    """Test: func returns list object"""
    tags = get_or_create_tags(5)
    assert isinstance(tags, list)


def test_get_or_create_vendors_returns_right_amount(vendor_client):
    """Test: func returns right vendors amount"""
    vendors = get_or_create_vendors(10)
    assert len(vendors) == 9


def test_get_or_create_vendors_returns_list():
    """Test: func returns list object"""
    vendors = get_or_create_vendors(3)
    assert isinstance(vendors, list)

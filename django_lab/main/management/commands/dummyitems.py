import sys
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from ...models import Product, Category, Tag
from faker import Faker
from random import choice, randint

# This constants provide max count of instance will create in db

CATEGORIES_AMOUT = 6
TAGS_AMOUNT = 10
VENDORS_AMOUNT = 5

fake = Faker(['ru_RU', 'en_US'])
Faker.seed(0)


def get_or_create_categories(amount: int) -> list:
    categories_qs = Category.objects.all()
    categories_list = []
    if len(categories_qs) >= amount:
        categories_list = list(categories_qs)
    else:
        for i in range(amount - len(categories_qs)):
            categories_list.append(
                Category.objects.create(
                    name=fake['ru_RU'].word(),
                    slug=f'category_{i + 1}'
                )
            )
    return categories_list


def get_or_create_tags(amount: int) -> list:
    tags_qs = Tag.objects.all()
    tags_list = []
    if len(tags_qs) >= amount:
        tags_list = list(tags_qs)
    else:
        for _ in range(amount - len(tags_qs)):
            tags_list.append(
                Tag.objects.create(
                    name=fake['ru_RU'].word()
                )
            )
    return tags_list


def get_or_create_vendors(amount: int) -> list:
    vendors_qs = User.objects.filter(profile__vendor=True)
    vendors_list = []
    if len(vendors_qs) >= amount:
        vendors_list = list(vendors_list)
    else:
        for _ in range(amount - len(vendors_qs)):
            user = User.objects.create_user(
                username=fake.simple_profile()['username'],
                password=fake.password(length=8),
            )
            user.profile.make_as_vendor()
            vendors_list.append(user)
    return vendors_list


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        try:
            i = int(count)
        except ValueError:
            print(u'n is to be a number!')
            sys.exit(1)

        categories: list = get_or_create_categories(CATEGORIES_AMOUT)
        tags: list = get_or_create_tags(TAGS_AMOUNT)
        vendors: list = get_or_create_vendors(VENDORS_AMOUNT)

        for _ in range(i):
            product = Product.objects.create(
                category=choice(categories),
                vendor=choice(vendors),
                name=fake['ru_RU'].word(),
                description=fake['ru_RU'].paragraph(nb_sentences=1),
                price=randint(100, 2000),
            )
            product.tags.set([choice(tags)])

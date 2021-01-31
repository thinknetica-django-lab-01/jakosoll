import sys
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from ...models import Product, Category, Tag
from faker import Faker
from random import choice, randint


fake = Faker(['ru_RU', 'en_US'])
Faker.seed(0)


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

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())
        vendor = User.objects.first()  # TODO: изменить на all, когда буду тестировать на большем кол-ве пользователей

        for _ in range(i):
            product = Product.objects.create(
                category=choice(categories),
                vendor=vendor,
                name=fake['ru_RU'].word(),
                description=fake['ru_RU'].paragraph(nb_sentences=1),
                price=randint(100, 2000),
            )
            product.tags.set([choice(tags)])

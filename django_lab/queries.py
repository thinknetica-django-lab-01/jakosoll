from main.models import Product
from main.models import Category
from main.models import Tag


category1 = Category.objects.create(name='Category 1', slug='category-1')
category2 = Category.objects.create(name='Category 2', slug='category-2')

product1 = Product(name='product 1', price=100, category=category1)
product1.save()
product2 = Product.objects.create(name='product 2', price=200, category=category2)

tag1 = Tag(name='tag 1')
tag1.save()
tag2 = Tag(name='tag 2')
tag2.save()

product1.tags.add(tag1)
product2.tags.add(tag1, tag2)

q = Product.objects.get(pk=1)
# <Product: product 1>

q = Product.objects.filter(tags=tag2)
# Получаем только второй товар <QuerySet [<Product: product 2>]>

q = Product.objects.filter(tags=tag1)
# Получаем оба товара <QuerySet [<Product: product 2>, <Product: product 1>]>

q = Product.objects.filter(category=category1)
# <QuerySet [<Product: product 1>]>

q = Category.objects.filter(product__name='product 1')
# <QuerySet [<Category: Category 1>]>

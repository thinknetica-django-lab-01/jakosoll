from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Product(models.Model):
    """product's model"""
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    vendor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Продавец')
    name = models.CharField('Название', max_length=40, db_index=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2, help_text='Укзажите сумму в '
                                                                                       'рублях')
    amount = models.PositiveIntegerField('Количество', default=1, help_text='Укажите ко-во товара')
    created = models.DateTimeField('Добавлен', auto_now_add=True)
    updated = models.DateTimeField('Последнее обновление', auto_now=True)
    tags = models.ManyToManyField('Tag', verbose_name='Теги')
    available = models.BooleanField(default=True)
    view_counter = models.PositiveIntegerField('Просмотры', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-updated']

    def get_absolute_url(self):
        return reverse('goods_detail', kwargs={'pk': self.id})


class Category(models.Model):
    """category's model"""
    name = models.CharField('Категория', max_length=20, db_index=True)
    slug = models.SlugField('url', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Profile(models.Model):
    """vendor's model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('Информация', max_length=500, blank=True)
    location = models.CharField('Местоположение', max_length=30, blank=True)
    vendor = models.BooleanField('Является ли продавцом', default=False)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    """"""
    name = models.CharField("Тег", max_length=30)

    def __str__(self):
        return self.name


class ProductSubscriber(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')


@receiver(post_save, sender=User)
def add_user_profile_and_perms(sender, instance, created, **kwargs):
    if created:
        common_users, group_created = Group.objects.get_or_create(name='common users')
        instance.groups.add(common_users)
        if group_created:
            perms = ('add_profile', 'change_profile')
            permissions_queryset = Permission.objects.filter(codename__in=perms)
            common_users.permissions.set(permissions_queryset)


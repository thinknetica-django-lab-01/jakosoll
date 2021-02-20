from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Product(models.Model):
    """
    Includes single product's entity,
    related:

    :class:`main.Category`,
    :class:`main.Tag`,
    :class:`auth.User`

    """
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
        """
        Метод возвращает абсолютный url :class:'Product'
        """
        return reverse('goods_detail', kwargs={'pk': self.id})


class Category(models.Model):
    """
    Includes single category's entity


    """
    name = models.CharField('Категория', max_length=20, db_index=True)
    slug = models.SlugField('url', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Profile(models.Model):
    """
    Includes single profile's entity.
    related:

    :class:`auth.User`

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('Информация', max_length=500, blank=True)
    location = models.CharField('Местоположение', max_length=30, blank=True)
    vendor = models.BooleanField('Является ли продавцом', default=False)

    def __str__(self):
        return self.user.username

<<<<<<< HEAD
    def make_as_vendor(self) -> None:
        """
        The method defines the user as the vendor

        :return None: 
        """
        if not self.vendor:
            self.vendor = True
            sellers, group_created = Group.objects.get_or_create(name='sellers')
            self.user.groups.add(sellers)
            if group_created:
                perms = ('add_product', 'change_product')
                permissions_queryset = Permission.objects.filter(codename__in=perms)
                sellers.permissions.set(permissions_queryset)
            self.save()

    @property
    def is_vendor(self) -> bool:
        """
        The property returns is a user as a vendor or not
        """
        return self.vendor


class Tag(models.Model):
    """
    Includes single tag's entity.
    """
    name = models.CharField("Тег", max_length=30)

    def __str__(self):
        return self.name


class ProductSubscriber(models.Model):
    """
    Includes single subscriber's entity.
    related:

    :class:`auth.User`

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')


@receiver(post_save, sender=User)
def add_user_profile_and_perms(sender, instance, created, **kwargs) -> None:
    """
    Post signal function adds new user in 'common users'.
    If group does not exists, it will be created
    """
    if created:
        common_users, group_created = Group.objects.get_or_create(name='common users')
        instance.groups.add(common_users)
        if group_created:
            perms = ('add_profile', 'change_profile')
            permissions_queryset = Permission.objects.filter(codename__in=perms)
            common_users.permissions.set(permissions_queryset)


@receiver(post_save, sender=User)
def update_or_create_user_profile(sender, instance, **kwargs) -> None:
    """Function adds profile when user created"""
    Profile.objects.update_or_create(user=instance)

# Generated by Django 3.1.5 on 2021-02-15 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210214_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='vendor',
            new_name='_vendor',
        ),
    ]

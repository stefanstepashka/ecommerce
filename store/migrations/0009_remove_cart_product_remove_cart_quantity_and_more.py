# Generated by Django 4.1.3 on 2022-12-21 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]

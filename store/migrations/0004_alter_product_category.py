# Generated by Django 4.1.3 on 2022-12-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('WHISKEY', 'Whiskey'), ('TEQUILLA', 'Tequilla'), ('RUM', 'Rum'), ('WINE', 'Wine'), ('VODKA', 'Vodka'), ('LIQUER', 'Liquer')], max_length=40),
        ),
    ]

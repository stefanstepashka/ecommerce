# Generated by Django 4.1.3 on 2022-12-20 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_product_id_alter_product_category_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='orders',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='store.product'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 2.2.14 on 2021-05-15 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='zipcode',
        ),
    ]
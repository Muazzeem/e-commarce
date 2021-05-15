# Generated by Django 3.2.3 on 2021-05-15 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='orderItem',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='orderItem',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='store.orderitem'),
            preserve_default=False,
        ),
    ]
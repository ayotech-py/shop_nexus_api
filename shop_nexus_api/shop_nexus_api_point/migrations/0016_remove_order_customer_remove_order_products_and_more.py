# Generated by Django 4.2.1 on 2023-06-14 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_nexus_api_point', '0015_alter_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='orderItem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop_nexus_api_point.orderitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop_nexus_api_point.customer'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ManyToManyField(to='shop_nexus_api_point.product'),
        ),
    ]
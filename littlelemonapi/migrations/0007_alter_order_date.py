# Generated by Django 4.2.7 on 2023-12-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('littlelemonapi', '0006_remove_order_total_remove_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True, db_index=True),
        ),
    ]
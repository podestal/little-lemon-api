# Generated by Django 4.2.7 on 2023-12-02 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('littlelemonapi', '0002_alter_cart_unique_together_cartitem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='unit_price',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='littlelemonapi.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]
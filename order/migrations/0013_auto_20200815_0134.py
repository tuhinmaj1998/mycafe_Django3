# Generated by Django 3.0.8 on 2020-08-14 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_orderproduct_discountoff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='discountOff',
            new_name='productDiscountOff',
        ),
    ]

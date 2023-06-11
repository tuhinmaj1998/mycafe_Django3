# Generated by Django 3.0.8 on 2020-08-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_deliverylimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverylimit',
            name='min_order_to_assign',
            field=models.PositiveSmallIntegerField(default=4, verbose_name='Min Order to Trigger Schedule'),
            preserve_default=False,
        ),
    ]
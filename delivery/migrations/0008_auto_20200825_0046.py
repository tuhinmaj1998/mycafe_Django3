# Generated by Django 3.0.8 on 2020-08-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20200825_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverypartnerschedule',
            name='confirmOTP',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

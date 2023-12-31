# Generated by Django 3.0.8 on 2020-08-24 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_auto_20200824_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='userAddress',
        ),
        migrations.AddField(
            model_name='order',
            name='houseNo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='locationAddress',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
